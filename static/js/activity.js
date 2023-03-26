$(document).on("mouseenter", ".botName", function getLogs() {
    document.getElementById('logsView').innerHTML = "";
     var bot_id = $(this).data('id');
     console.log(bot_id);
     setTimeout(function(){
     $.ajax({
                type: 'GET',
                async: true,
                url: '/activity/',
                data: {'bot_id': bot_id, 'logs': true},
                headers:{
                    "X-CSRFToken": csrftoken
                },
                success: function(data) {
                    data.forEach(makeLogs);
                },
            dataType: 'json',
            });

     function makeLogs(value, index, array) {
        var element = document.getElementById('logsView');
        var pElem = document.createElement('p');
        pElem.className = 'logs';
        pElem.innerHTML = value;
        element.appendChild(pElem);
     }
     },1000);
});


$(document).on("mouseenter", ".botID", function getActions() {
     document.getElementById('actionID').innerHTML = "";
     document.getElementById('actionDate').innerHTML = "";
     var bot_id = $(this).data('id');
     console.log(bot_id);
     setTimeout(function(){
     $.ajax({
                type: 'GET',
                async: true,
                url: '/activity/',
                data: {'bot_id': bot_id, 'actions': true},
                headers:{
                    "X-CSRFToken": csrftoken
                },
                success: function(data) {
                    data.forEach(makeActions);
                },
            dataType: 'json',
            });

     function makeActions(value, index, array) {
        var element = document.getElementById('actionID');
        var pElem = document.createElement('p');
        pElem.className = 'actions';
        pElem.innerHTML = value.action_id;
        element.appendChild(pElem);

        var element2 = document.getElementById('actionDate');
        var pElem2 = document.createElement('p');
        pElem2.className = 'actions';
        pElem2.innerHTML = value.action_date;
        element2.appendChild(pElem2);
     }
     },1000);
});


$(document).ready(function StartAjax(){
        setTimeout(function(){

              $.ajax({
                type: 'GET',
                async: true,
                url: '/activity/',
                data: {'bot_id': null},
                headers:{
                    "X-CSRFToken": csrftoken
                },
                success: function(data) {
                    makeProgress(data);
                    StartAjax();
                },
            dataType: 'json',
            });
     var tableRef = document.getElementById('activity-dataTable').getElementsByTagName('tbody')[0];
     function makeProgress(value, index, array) {
        console.log(value.all_bots);
        var all_tr = document.querySelectorAll(".odd.gradeX");
        var all_tr_copy = document.querySelectorAll(".odd.gradeX");
        console.log(all_tr);
        for (k in all_tr_copy) {
            if (all_tr_copy.hasOwnProperty(k)) {
                var bot_id = all_tr_copy[k].getAttribute("data-id");
                if (!value.all_bots.includes(bot_id)) {
                    all_tr[k].remove()
                    console.log('removed');
                } else
                {
                    console.log('not removed');
                }
            }
        }
        for (bot in value.tracks) {
            if (value.tracks.hasOwnProperty(bot)) {
                console.log(value.tracks[bot]['bot_id']);
                var progress_val = value.tracks[bot]['progress'];
                for (progress in all_tr) {
                    if (all_tr.hasOwnProperty(progress)) {
                        if (all_tr[progress].getAttribute("data-id") === value.tracks[bot]['bot_id']) {
                            var progress_bar = all_tr[progress].querySelectorAll('.progress-bar');
                            console.log(progress_bar);
                            progress_bar[0].setAttribute("style", "width: " +progress_val+"%;");
                            progress_bar[0].setAttribute("aria-valuenow", progress_val);
                            var progress_text = progress_bar[0].children;
                            console.log(progress_text);
                            progress_text[0].textContent=progress_val+"%";
                        }
                    }
                }
            }
        }
     }
     },5000);
});