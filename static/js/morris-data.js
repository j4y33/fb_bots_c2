$(function() {

    Morris.Area({
        element: 'morris-area-chart',
        data: [{
            period: '2012-10-01 9:00',
            likes: 45,
            comments: 30
        }, {
            period: '2012-10-01 10:00',
            likes: 57,
            comments: 35
        }, {
            period: '2012-10-01 11:00',
            likes: 120,
            comments: 90
        }],
        xkey: 'period',
        ykeys: ['likes', 'comments'],
        labels: ['LIKES', 'COMMENTS'],
        pointSize: 4,
        hideHover: 'auto',
        resize: true
    });

    Morris.Donut({
        element: 'morris-donut-chart',

        data: [{
            label: "BLOCKED",
            value: 12
        }, {
            label: "ACTIVE",
            value: 30
        }, {
            label: "INACTIVE/PAUSED",
            value: 20
        }],
        resize: true
    });

    Morris.Bar({
        element: 'morris-bar-chart-comp1',
        data: [{
            y: 'Pages',
            a: 100,
            b: 90
        }, {
            y: 'Groups',
            a: 75,
            b: 65
        }, {
            y: 'Walls',
            a: 50,
            b: 40
        }, {
            y: 'Posts(searches)',
            a: 75,
            b: 65
        }],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['Likes', 'Comments'],
        hideHover: 'auto',
        resize: true
    });
        Morris.Bar({
        element: 'morris-bar-chart-comp2',
        data: [{
            y: 'Pages',
            a: 100,
            b: 90
        }, {
            y: 'Groups',
            a: 75,
            b: 65
        }, {
            y: 'Walls',
            a: 50,
            b: 40
        }, {
            y: 'Posts(searches)',
            a: 75,
            b: 65
        }],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['Likes', 'Comments'],
        hideHover: 'auto',
        resize: true
    });

});
