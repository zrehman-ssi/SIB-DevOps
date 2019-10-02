import axios from '../../node_modules/axios'
import {router} from '../router'
const ApiService = {
  init() {
    axios.defaults.baseURL = 'http://127.0.0.1:5000';
  },


  setHeader() {
    this.init();
     axios.defaults.withCredentials=true;
     axios.defaults.headers.common["Access-Control-Allow-Headers"]= `Origin, X-Requested-With, Content-Type, Accept, Set-Cookie, Authorization`;
     axios.defaults.headers.common["Access-Control-Allow-Origin"]="*";
     axios.defaults.headers.common["Access-Control-Expose-Headers"]=`Set-Cookie`;
     axios.defaults.headers.common["Access-Control-Allow-Credentials"]=true;
  },

  query(resource, params) {
    this.setHeader();
    return axios.get(resource, params).catch(error => {
      throw new Error(`ApiService ${error}`);
    });
  },

  get(resource) {
    this.setHeader();
    return axios.get(`${resource}`).catch(error => {
      if(error.response.status===401) {
        router.push({name: 'login'});
      }
    });
  },

  post(resource, jsonData) {
    this.setHeader();
    return axios.post(`${resource}`, jsonData).catch(error => {
      if(error.response.status===401) {
        router.push({name: 'login'});
      }
    });
  },

  update(resource, slug, params) {
    this.setHeader();
    return axios.put(`${resource}/${slug}`, params).catch(error => {
      if(error.response.status===401) {
        router.push({name: 'login'});
      }
    });
  },

  put(resource, params) {
    this.setHeader();
    return axios.put(`${resource}`, params).catch(error => {
      if(error.response.status===401) {
        router.push({name: 'login'});
      }
    });
  },

  delete(resource) {
    this.setHeader();
    return axios.delete(resource).catch(error => {
      if(error.response.status===401) {
        router.push({name: 'login'});
      }
    });
  }
};

export default ApiService;
