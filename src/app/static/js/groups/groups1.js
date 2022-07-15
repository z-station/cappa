var tableFilter = {
    search: function(event){
        event.preventDefault()
        tableFilter.resetSearch()
        var searchStr = document.getElementById('js__search-input').value
        if(searchStr){
            var searchValues = searchStr.toLowerCase().split(',');
            document.querySelectorAll('.js__username').forEach(function(elem){
                for(let i=0; i < searchValues.length; i++){
                    var showElem = false
                    if(elem.textContent.toLowerCase().indexOf(searchValues[i].trim()) != -1 ){
                        showElem = true
                        break
                    }
                }
                if(!showElem){
                    elem.parentElement.style.display = "none";
                }
            })
        }
    },
    resetSearch: function(){
        document.querySelectorAll('.js__username').forEach(function(elem){
            elem.parentElement.style.display = "table-row";
        })
    }
}

var showLoader = () => {
    document.querySelector('.js__loader').style.display = 'flex';
}
var hideLoader = () => {
    document.querySelector('.js__loader').style.display = 'none';
}