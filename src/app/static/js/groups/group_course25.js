const $ = window.jQuery;
const API_URL = document.getElementById('course-table').dataset.apiUrl;     // задаётся в шаблоне
const AUTH_HEADER = { Authorization: `Token ${window.authToken}` };
const TH_SELECTOR = '.js__course__table thead th[data-topic]';
const TD_SELECTOR = '.js__course__table tbody td.js__taskitem';
const reviewStatuses = {
    ready: 'ready',
    review: 'review',
    checked: 'checked',
    awaitingCheck: ['ready', 'review']
};
const checkMethods = {
    tests: 'tests',
    review: 'review',
    testsAndReview: 'tests_and_review',
    testsMethods:  ['tests', 'tests_and_review'],
    reviewMethods: ['review', 'tests_and_review']
};

/*Загрузка статистики*/
function loadStatistics(silent = false) {
    if (!silent) showLoader();
    /* очистить старые значения */
    document.querySelectorAll(TD_SELECTOR).forEach(td => {
        td.innerHTML = '';
        td.dataset.score = '';
        td.className = td.className.replace(/\bs\-\w+|\bawaiting\-check/g, '');
        td.removeAttribute('title');
    });

    $.ajax({
        url: API_URL,
        type: 'GET',
        dataType: 'json',
        headers: AUTH_HEADER
    })
        .done(updateTable)
        .fail(xhr =>
            console.error('statistics API error', xhr.status, xhr.responseText))
        .always(hideLoader);
}

// Синхронизация выбора тем
const topicFilterPanel = document.getElementById('js__topic-filter-panel');
const allCheckbox = topicFilterPanel.querySelector('input[value="all"]');

topicFilterPanel.addEventListener('change', e => {
  const input = e.target;
  const isAll = input.value === 'all';

  const allCheckbox = topicFilterPanel.querySelector('input[value="all"]');
  const otherCheckboxes = topicFilterPanel.querySelectorAll('.js__topic-filter-checkbox:not([value="all"])');

  if (isAll) {
    // Очистить выбранные темы
    selectedTopics.clear();
    // Снять галочки с других чекбоксов
    otherCheckboxes.forEach(cb => cb.checked = false);
    // Отметить "все темы"
    allCheckbox.checked = true;
  } else {
    if (input.checked) {
      selectedTopics.add(input.value);
    } else {
      selectedTopics.delete(input.value);
    }
    // Снять "все темы", если выбрана хоть одна
    allCheckbox.checked = false;
  }
  // если ни одна тема не выбрана — активировать "все темы"
  if (selectedTopics.size === 0) {
    allCheckbox.checked = true;
  }
  applyTopicFilter();
});


/*Заполнение таблицы*/
function updateTable(resp) {
    const tasksMap = resp.tasks_max_points || {};
    const stats    = resp.stats           || resp;
    window.tasksMaxPoints = { ...tasksMap };

    const tbody = document.querySelector('.js__course__table tbody');
    const frag  = document.createDocumentFragment();

    for (const [userId, userData] of Object.entries(stats)) {
        const tr = document.getElementById(`js__member-${userId}`);
        if (!tr) continue;
        frag.appendChild(tr);
        let solved = 0, scoreSum = 0;

        for (const [taskId, data] of Object.entries(userData)) {
            if (!(taskId in window.tasksMaxPoints)) {
                window.tasksMaxPoints[taskId] = data.max_score;
            }

            const td = tr.querySelector(`.js__taskitem__${taskId}`);
            if (!td) continue;

            const overdue = data.due_date &&
                            (new Date(data.created) > new Date(data.due_date));
            if (overdue) td.classList.add('s-grey');

            const th = document.querySelector(`th[data-taskitem-id="${taskId}"]`);
            if (th) {
                td.title = [
                    tr.querySelector('.js__username').innerText,
                    new Date(data.created).toLocaleString(),
                    th.querySelector('a').dataset.taskitemTitle,
                    `Тема: ${th.dataset.topicTitle}`,
                    overdue ? 'Решение отправлено после дедлайна' : ''
                ].filter(Boolean).join('\n');
            }

            // Создание содержимого ячейки
            const cell = window.userIsTeacher
                ? Object.assign(document.createElement('a'), {
                    href: `/solutions/${data.id}/`,
                    target: '_blank'
                })
                : document.createElement('div');

            let localScore = 0;
            let isSolved = false;

            // Режим проверки вручную
            if (checkMethods.reviewMethods.includes(data.score_method)) {
                if (data.review_status === reviewStatuses.checked) {
                    if (data.review_score == null) {
                        cell.textContent = '✔';
                        td.classList.add('s-green');
                        isSolved = true;
                    } else if (data.review_score === data.max_score) {
                        cell.textContent = '+';
                        td.classList.add('s-green');
                        localScore = data.review_score;
                        isSolved = true;
                    } else if (data.review_score === 0) {
                        cell.textContent = '-';
                        td.classList.add('s-red');
                    } else {
                        cell.textContent = data.review_score;
                        td.classList.add('s-yellow');
                        localScore = data.review_score;
                        isSolved = true;
                    }
                } else if (reviewStatuses.awaitingCheck.includes(data.review_status)) {
                    td.classList.add('awaiting-check', 's-cyan');
                }
            } else {
                // Автоматическая проверка (тесты)
                if (data.testing_score === data.max_score) {
                    cell.textContent = '+';
                    td.classList.add('s-green');
                    localScore = data.testing_score;
                    isSolved = true;
                } else if (data.testing_score === 0) {
                    cell.textContent = '-';
                    td.classList.add('s-red');
                } else {
                    cell.textContent = data.testing_score;
                    td.classList.add('s-yellow');
                    localScore = data.testing_score;
                    isSolved = true;
                }
            }
            td.append(cell);
            td.dataset.score = localScore;

            if (!overdue && isSolved) solved += 1;
            if (!overdue) scoreSum += localScore;
        }
        tr.querySelector('.js__total_solved_tasks').textContent = solved;
        tr.querySelector('.js__total_score').textContent = scoreSum.toFixed(1);
    }
    tbody.innerHTML = '';
    tbody.appendChild(frag);
    $('.js__tablesorter').trigger('update');
    buildTopicFilter();
    applyTopicFilter();
    syncFakeScrollbar();
}


/*Фильтр тем*/
let filterBuilt    = false;
let topicsCache    = null;
let selectedTopics = new Set();

function buildTopicFilter() {
  if (filterBuilt) return;

  const panel   = document.getElementById('js__topic-filter-panel');
  const wrap    = document.getElementById('js__topic-cols');
  const search  = document.getElementById('topic-search');

  if (!topicsCache) {
    topicsCache = {};
    document.querySelectorAll(TH_SELECTOR).forEach(th => {
      topicsCache[th.dataset.topic] =
            th.dataset.topicTitle
         || th.querySelector('a').dataset.topicTitle
         || th.querySelector('a').textContent.trim();
    });
    if (!Object.keys(topicsCache).length) return;   // thead ещё не готов
  }

  Object.entries(topicsCache).forEach(([num, text]) => {
    const label = document.createElement('label');
    label.className = 'topic-label';
    label.innerHTML =
      `<input type="checkbox" class="js__topic-filter-checkbox" value="${num}">
       ${text}`;
    wrap.appendChild(label);
  });

  /*живой поиск */
  function filterTopicLabels() {
    const q = search.value.toLowerCase().trim();
    const parts = q.split(/\s+/).filter(Boolean);

    wrap.querySelectorAll('label.topic-label').forEach(lbl => {
      const hit = !parts.length ||
                  parts.every(p => lbl.textContent.toLowerCase().includes(p));
      lbl.style.display = hit ? '' : 'none';
    });
  }

  search.addEventListener('input',  filterTopicLabels);
  search.addEventListener('keyup',  filterTopicLabels);
  filterTopicLabels();

  /*кнопка «Фильтр тем»*/
  document.getElementById('js__topic-filter-btn')
          .addEventListener('click', () =>
            panel.style.display = panel.style.display === 'none' ? 'block'
                                                                 : 'none');
  filterBuilt = true;
}

/*Показ / скрытие колонок по чек-боксам*/
function applyTopicFilter() {
    const showAll = selectedTopics.size === 0;
    const topicsToShow = [...selectedTopics];

    document.querySelectorAll(TH_SELECTOR).forEach(th => {
        th.style.display = showAll || topicsToShow.includes(th.dataset.topic) ? '' : 'none';
    });
    document.querySelectorAll(TD_SELECTOR).forEach(td => {
        td.style.display = showAll || topicsToShow.includes(td.dataset.topic) ? '' : 'none';
    });
    recalcTotals();
    syncFakeScrollbar();
}

function recalcTotals() {
    document.querySelectorAll('.js__course__table tbody tr').forEach(tr => {
        if (tr.classList.contains('totals-row')) return;
        let solved = 0, sum = 0;
        tr.querySelectorAll('td.js__taskitem').forEach(td => {
            if (td.style.display === 'none') return;
            const val = td.dataset.score;
            if (td.classList.contains('s-green') || td.classList.contains('s-yellow')) {
                solved += 1;
            }
            const num = parseFloat(val);
            if (!isNaN(num)) {
                sum += num;
            }
        });
        tr.querySelector('.js__total_solved_tasks').textContent = solved;
        tr.querySelector('.js__total_score').textContent = sum.toFixed(1);
    });
    //Обновляем итоговую строку "Всего"
    const visibleTasks = document.querySelectorAll('th[data-topic]:not([style*="display: none"])');
    const tasksCount = visibleTasks.length;
    let maxPointsSum = 0;
    visibleTasks.forEach(th => {
        const taskId = th.dataset.taskitemId;
        if (window.tasksMaxPoints && taskId in window.tasksMaxPoints) {
            maxPointsSum += window.tasksMaxPoints[taskId];
        }
    });
    //Обновляем ячейки итогов
    document.querySelector('.totals-row .js__total_tasks_count').textContent = tasksCount;
    document.querySelector('.totals-row .js__total_points_sum').textContent = maxPointsSum.toFixed(1);
}



/*Кнопка «Обновить» и поиск по участникам*/
document.getElementById('js__refresh-btn')
        .addEventListener('click', () => loadStatistics(true));

document.getElementById('filter-box')
        .addEventListener('input', function () {
    const q = this.value.toLowerCase().trim();
    const parts = q.split(',').map(p => p.trim()).filter(Boolean);
    document.querySelectorAll('.js__course__table tbody tr').forEach(tr => {
        const name = tr.querySelector('.js__username').textContent.toLowerCase();
        const show = !parts.length || parts.some(p => name.includes(p));
        tr.style.display = show ? '' : 'none';
    });
});

let cachedElements = null;
let resizeTimeout;
const RESIZE_DELAY = 100;

function cacheElements() {
    cachedElements = {
        table: document.querySelector('.js__course__table'),
        fakeTable: document.querySelector('.js__course__fake-table'),
        topScrollContainer: document.querySelector('.js__course__fake-table-container'),
        bottomScrollContainer: document.querySelector('.js__course__table-container')
    };
}

function syncFakeScrollbar() {
    if (!cachedElements) cacheElements();
    const { table, fakeTable } = cachedElements;

    if (table && fakeTable) {
        fakeTable.style.width = `${table.scrollWidth}px`;
    }
    toggleFakeScrollbarVisibility();
}

function toggleFakeScrollbarVisibility() {
    if (!cachedElements) cacheElements();
    const { bottomScrollContainer, topScrollContainer } = cachedElements;

    if (!bottomScrollContainer || !topScrollContainer) return;

    const hasScroll = bottomScrollContainer.scrollWidth > bottomScrollContainer.clientWidth;
    topScrollContainer.style.display = hasScroll ? 'block' : 'none';
}

function attachScrollbarSync() {
    if (!cachedElements) cacheElements();
    const { topScrollContainer, bottomScrollContainer } = cachedElements;

    if (!topScrollContainer || !bottomScrollContainer) return;

    const syncScroll = (source, target) => {
        source.addEventListener('scroll', () => {
            target.scrollLeft = source.scrollLeft;
        });
    };
    syncScroll(topScrollContainer, bottomScrollContainer);
    syncScroll(bottomScrollContainer, topScrollContainer);
}


/*Инициализация*/
document.addEventListener('DOMContentLoaded', () => {
    cacheElements();
    syncFakeScrollbar();
    attachScrollbarSync();
    loadStatistics();

    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(syncFakeScrollbar, RESIZE_DELAY);
    });
});