import location from "./data.js";

function getProvinces() {
    return Object.keys(location);
}

function getDistricts(province) {
    try {
        const data = location[province];
        return Object.keys(data);
    } catch (error) {
        console.log(error);
        return [];
    }
}

function getSectors(province, district) {
    try {
        const data = location[province][district];
        return Object.keys(data);
    } catch (error) {
        console.log(error);
        return [];
    }
}

function getCells(province, district, sector) {
    try {
        const data = location[province][district][sector];
        return Object.keys(data);
    } catch (error) {
        console.log(error);
        return [];
    }
}

function getVillages(province, district, sector, cell) {
    try {
        const data = location[province][district][sector][cell];
        return data;
    } catch (error) {
        console.log(error);
        return [];
    }
}

$(document).ready(function () {
    function loadProvinces(provinces) {
        const PROVINCES = $("#id_province")
        PROVINCES.empty();

        provinces.forEach(province => {
            PROVINCES.append($("<option class='province' value='" + province + "'>" + province + "</option>"))
        });

    }

    function loadDistricts(districts) {
        const DISTRIC = $("#id_district")
        DISTRIC.empty();

        districts.forEach(district => {
            DISTRIC.append($("<option value='" + district + "'>" + district + "</option>"))
        });

    }

    function loadSectors(sectors) {
        const SECTOR = $("#id_sector")
        SECTOR.empty();

        sectors.forEach(sector => {
            SECTOR.append($("<option value='" + sector + "'>" + sector + "</option>"))
        });

    }

    loadProvinces(getProvinces());
    $("#id_province").click(() => {
        const selectedProvinceValue = $('#id_province').val();
        if (selectedProvinceValue != null) {
            loadDistricts(getDistricts(selectedProvinceValue));
        }
    });

    $("#id_district").click(() => {
        const selectedProvinceValue = $('#id_province').val();
        if (selectedProvinceValue != null) {
            const selectedDistrictValue = $('#id_district').val();
            if (selectedDistrictValue != null) {
                loadSectors(getSectors(selectedProvinceValue, selectedDistrictValue));
            }
        }
    });
});