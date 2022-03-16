var i = 1;
function childrenRow() {
    i++;
    $('#childTable').find('tbody').append('<tr><td scope="row">#' +
        '</td><td><input class="border-0 w-100" data-column="a1_1" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="a1_2" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="a1_3" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="a1_4" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="a1_5" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="a1_6" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="a1_7" type="text"\n' + 'placeholder=""></td>\n' +
        '<td \n' + 'class="fa fa-plus-circle f-20 txt-primary"\n' +
        'id="addrow" onclick="childrenRow()"\n' + '/></td>\n' +
        '<td><i class="fa fa-close f-20 txt-danger del-row"></i></td></tr>');
}

var j = 1;
function childrenTable() {
    j++;
    $('#childTable1').find('tbody').append('<tr><td scope="row">#</td>' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td \n' +'class="fa fa-plus-circle f-20 txt-primary"\n' +
        'id="addrow1" onclick="childrenTable()"\n' +'/></td>\n' +
        '<td><i class="fa fa-close f-20 txt-danger del-row"></i></td></tr>');
}

var a = 1;
function childrentable() {
    a++;
    $('#childTable2').find('tbody').append('<tr><th class="table-primary" scope="row">' + a +
        '</th><td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td \n' + 'class="fa fa-plus-circle f-20 txt-primary"\n' +
        'id="addrow1" onclick="childrentable()"\n' + '/></td>\n' +'</td></tr>');
}

var x = 1;
function childrentabl1() {
    x++;
    $('#childTable3').find('tbody').append('<tr><th scope="row">' + x +
        '</th>' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td \n' + 'class="fa fa-plus-circle f-20 txt-primary"\n' +
        'id="addrow3" onclick="childrentabl1()"\n' + '/></td>\n' +'</td></tr>');
}
var y = 1;
function childrentabl2() {
    y++;
    $('#childTable4').find('tbody').append('<tr><th scope="row">' + y +
        '</th>' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td \n' + 'class="fa fa-plus-circle f-20 txt-primary"\n' +
        'id="addrow4" onclick="childrentabl2()"\n' + '/></td>\n' +'</td></tr>');
}
var z = 1;
function childrentabl3() {
    z++;
    $('#childTable5').find('tbody').append('<tr><th scope="row">' + z +
        '</th>' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td \n' + 'class="fa fa-plus-circle f-20 txt-primary"\n' +
        'id="addrow5" onclick="childrentabl3()"\n' + '/></td>\n' +'</td></tr>');
}
var q = 1;
function childrentabl4() {
    q++;
    $('#childTable6').find('tbody').append('<tr><th scope="row">' + q +
        '</th>' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td \n' + 'class="fa fa-plus-circle f-20 txt-primary"\n' +
        'id="addrow6" onclick="childrentabl4()"\n' + '/></td>\n' +'</td></tr>');
}
var r = 1;
function childrentabl5() {
    r++;
    $('#childTable7').find('tbody').append('<tr><th scope="row">' + r +
        '</th>' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td \n' + 'class="fa fa-plus-circle f-20 txt-primary"\n' +
        'id="addrow7" onclick="childrentabl5()"\n' + '/></td>\n' +'</td></tr>');
}
var t = 1;
function childrentabl6() {
    t++;
    $('#childTable8').find('tbody').append('<tr data-obj =-1><td scope="row">#'+
        '</td>' +
        '<td><input class="border-0 w-100 b8_1" data-column="b8_1" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100 b8_2" data-column="b8_2" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100 b8_3" data-column="b8_3" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100 b8_4" data-column="b8_4" type="text"\n' + 'placeholder=""></td>\n' +
        '<td \n' + 'class="fa fa-plus-circle f-20 txt-primary"\n' +

        'id="addrow8" onclick="childrentabl6()"\n' + '/></td>\n'+
        '<td><i class="fa fa-close f-20 txt-danger del-row"></i></td></tr>');
}
var h = 1;
function childrentabl7() {
    h++;
    $('#childTable9').find('tbody').append('<tr><td scope="row">#'+
        '</td>' +
        '<td><input class="border-0 w-100 b9_1" data-column="b9_1"  type="number"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100 b9_2" data-column="b9_2" type="number"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100 b9_3" data-column="b9_3" type="number"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100 b9_4" data-column="b9_4" type="number"\n' + 'placeholder=""></td>\n' +
        '<td \n' + 'class="fa fa-plus-circle f-20 txt-primary"\n' +
        'id="addrow9" onclick="childrentabl7()"\n' + '/></td>\n' +
        '<td><i class="fa fa-close f-20 txt-danger del-row"></i></td></tr>');
}
var l = 1;
function childrentablseven() {
    l++;
    $('#childTableTen').find('tbody').append('<tr><td scope="row">#'+
        '</td>' +
        '<td><input class="border-0 w-100" data-column="b17_1" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="b17_2" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="b17_3" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="b17_4" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="b17_5" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="b17_6" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="b17_7" type="text"\n' + 'placeholder=""></td>\n' +
        '<td \n' + 'class="fa fa-plus-circle f-20 txt-primary"\n' +
        'id="addrowten" onclick="childrentablseven()"\n' + '/></td>\n' +
         '<td><i class="fa fa-close f-20 txt-danger del-row"></i></td></tr>');
}
var l = 1;
function childrentableight() {
    l++;
    $('#childTableEleven').find('tbody').append('<tr><td scope="row">#'+
        '</td>' +
        '<td><input class="border-0 w-100" data-column="b18_1" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="b18_2" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="b18_3" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100 " data-column="b18_4" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" data-column="b18_5" type="text"\n' + 'placeholder=""></td>\n' +
        '<td \n' + 'class="fa fa-plus-circle f-20 txt-primary"\n' +
        'id="addroweleven" onclick="childrentableight()"\n' + '/></td>\n' +
        '<td><i class="fa fa-close f-20 txt-danger del-row"></i></td></tr>');
}

var l = 1;
function childrenRow_pr() {
    l++;
    $('#childTable_pr1').find('tbody').append('<tr><td scope="row">#' +
        '</td>' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td \n' + 'class="fa fa-plus-circle f-20 txt-primary"\n' +
        'id="addroweleven" onclick="childrenRow_pr()"\n' + '/></td>\n' +
        '<td><i class="fa fa-close f-20 txt-danger del-row"></i></td></tr>');
}

var l = 1;
function childrenRow_pr2() {
    l++;
    $('#childTable_pd2').find('tbody').append('<tr><th scope="row">' + l +
        '</th>' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td><input class="border-0 w-100" type="text"\n' + 'placeholder=""></td>\n' +
        '<td \n' + 'class="fa fa-plus-circle f-20 txt-primary"\n' +
        'id="addroweleven" onclick="childrenRow_pr2()"\n' + '/></td>\n' +'</td></tr>');
}

