// import { createApp } from 'vue'
import { createStore } from 'vuex'
// import axios from "axios";

export default createStore({
    state () {
        return {
            cameras: []
        }
    },
    mutations: {
        setCameras (state, camera) {
            state.cameras.push(camera)
        }
    },
    actions: {
        addCamera({commit}, camera) {
            commit('setCameras', camera)
        }
    },
    getters: {
        getCameras(state) {
            return state.cameras
        }
    }
})

