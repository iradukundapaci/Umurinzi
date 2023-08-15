// data.js
// Import the data from data.json
import allData from "./data";

export function getProvinces() {
    return Object.keys(allData);
}

export function getDistricts(province) {
    try {
        const data = allData[province];
        return Object.keys(data);
    } catch (error) {
        console.log(error);
        return [];
    }
}

export function getSectors(province, district) {
    try {
        const data = allData[province][district];
        return Object.keys(data);
    } catch (error) {
        console.log(error);
        return [];
    }
}

export function getCells(province, district, sector) {
    try {
        const data = allData[province][district][sector];
        return Object.keys(data);
    } catch (error) {
        console.log(error);
        return [];
    }
}

export function getVillages(province, district, sector, cell) {
    try {
        const data = allData[province][district][sector][cell];
        return data;
    } catch (error) {
        console.log(error);
        return [];
    }
}
