import axios from 'axios'
import Cookie from '../Cookie'

const c = new Cookie()
const API_URL = c.getCookie('url')

export default class PostService {
    getURL() {
        return API_URL;
    }
    
    getPosts() {
        return axios.get(`${API_URL}/posts/`, c.getHeaders()).then(response => response.data);
    }

    getPost(pk) {
        return axios.get(`${API_URL}/posts/${pk}`, c.getHeaders()).then(response => response.data);
    }

    getPostsURL(url) {
        return axios.get(url, c.getHeaders()).then(response => response.data);
    }
}