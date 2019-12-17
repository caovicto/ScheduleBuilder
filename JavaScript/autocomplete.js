var optionList = ["Seattle", "Las Vegas", "New York", "Salt lake City"];

function fillDataList(box_name, data_list) {
    var container = document.getElementById(box_name),
    i = 0,
    len = optionList.length,
    dl = document.createElement(datalist);

    dl.id = data_list;
    for (; i < len; i += 1) {
        var option = document.createElement('option');
        option.value = option_list[i];
        dl.appendChild(option);
    }
    container.appendChild(dl);
}

fillDataList('major_selection', 'major_list');

