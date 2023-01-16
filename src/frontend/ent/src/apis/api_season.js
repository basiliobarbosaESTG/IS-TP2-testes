import axios from "axios";

const api_season = axios.create({
    baseUrl: 'http://localhost:20001/api/season/'
});

export default api_season;