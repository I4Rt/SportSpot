// import { createApp } from 'vue'
import {createStore} from 'vuex'
// import axios from "axios";

export default createStore({
    state () {
        return {
            tasks: [],
            cameras: [],
            rooms: [],
            sectors: [],
            sectorTypes: [],
            unusedCameras: {},
            usedCameras: {},
            refreshInterval: null,
        }
    },
    mutations: {
        removeCamera (state, id) {
            state.cameras = state.cameras.filter((camera) => camera.id !== id)
        },
        removeRoom (state, id) {
            state.rooms = state.rooms.filter((room) => room.id !== id)
        },
        removeTask (state, id) {
            state.tasks = state.tasks.filter((task) => task.id !== id)
        },
        removeSector (state, id) {
            state.sectors = state.sectors.filter((sector) => sector.id !== id)
        },
        updateCamera (state, oldCamera, newCamera) {
            oldCamera = newCamera
        },
        setCameras (state, camera) {
            state.cameras.push(camera)
        },
        setRooms (state, room) {
            state.rooms.push(room)
        },
        setSector (state, sector) {
            state.sectors.push(sector)
        },
        setTask (state, task) {
            state.tasks.push(task)
        },
        setRefreshInterval (state, interval) {
          state.refreshInterval = interval
        },
        clearRefreshInterval (state) {
            clearInterval(state.refreshInterval)
            state.refreshInterval = null
        }
    },
    actions: {
        addCamera({commit}, newCamera) {
            commit('setCameras', newCamera)
        },
        refreshToken(){
            let resp
            fetch('http://localhost:5000/refresh', {
                method: 'GET',
                credentials:"include",
                cors: 'no-cors',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8',
                },
            })
                .then(response => response.json())
                .then(response => {
                    console.log(response)
                    resp = response
                })
            return resp
        },
        async removeCamera({commit}, id) {
            console.log('remove')
            await fetch(`http://localhost:5000/removeCamera?id=${id}`, {
                credentials: "include",
                method: 'GET',
                cors: 'no-cors',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8',
                },
            })
                .then(response => response.json())
                .then((response) => {
                    if (response.OperationStatus === "Done"){
                        commit('removeCamera', id)
                    }
                })
        },
        removeRoom({commit}, id) {
            fetch(`http://localhost:5000/removeRoom?id=${id}`, {
                credentials: "include",
                method: 'GET',
                cors: 'no-cors',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8',
                },
            })
                .then(response => response.json())
                .then((response) => {
                    if (response.OperationStatus === "Done"){
                        commit('removeRoom', id)
                    }
                })
        },
        removeTask({commit}, id) {
            fetch(`http://localhost:5000/removeTask?id=${id}`, {
                credentials: "include",
                method: 'GET',
                cors: 'no-cors',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8',
                },
            })
                .then(response => response.json())
                .then((response) => {
                    if (response.OperationStatus === "Done"){
                        commit('removeTask', id)
                    }
                })
        },
        removeSector({commit}, id) {
            return fetch(`http://localhost:5000/removeSector?id=${id}`, {
                credentials: "include",
                method: 'GET',
                cors: 'no-cors',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8',
                },
            })
                .then(response => response.json())
                .then((response) => {
                    if (response.OperationStatus === "Done") {
                        commit('removeSector', id)
                    }
                    return response
                })
        },
        addRoom({commit}, newRoom) {
            commit('setRooms', newRoom)
        },

    },
    getters: {
        getRefreshInterval(state){
            return state.refreshInterval
        },
        getCameras(state) {
            return state.cameras
        },
        getCameraByID: (state) => (id) => {
            return state.cameras.find(camera => camera.id === id)
        },
        getSectors(state) {
          return state.sectors
        },
        getSectorByID: (state) => (id) => {
            return state.sectors.find(sector => sector.id === id)
        },
        getSectorsByCameraID: (state) => (id) => {
            return state.sectors.filter(sector => sector.camId === id)
        },
        getSectorTypes(state) {
            return state.sectorTypes
        },
        getSectorTypeByID: (state) => (id) => {
            return state.sectorTypes.find(sectorType => sectorType.id === id)
        },
        getRooms(state) {
            return state.rooms
        },
        getRoomByID: (state) => (id) => {
            return state.rooms.find(room => room.id === id)
        },
        // getUnusedSectorByID: (state) => (id) => {
        //     for (let i = 0; i < state.unusedCameras.camerasList.length; i++){
        //         for (let j = 0; j < state.unusedCameras.camerasList[i].sectors.length; j++){
        //             if (state.unusedCameras.camerasList[i].sectors[j].id === id){
        //                 return state.unusedCameras.camerasList[i].sectors[j]
        //             }
        //         }
        //     }
        // },
        getUsedCameras(state) {
            return state.usedCameras.camerasList
        },
        getUnusedCameras(state) {
            return state.unusedCameras.camerasList
        },
        getTasks(state) {
            return state.tasks
        },
        getTaskByID: (state) => (id) => {
            return state.tasks.find(task => task.id === id)
        },
    },
})

