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
            roomTypes: [],
            unusedCameras: {},
            usedCameras: {},
            refreshInterval: null,
            authorized: false
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
        setCamera (state, camera) {
            state.cameras.push(camera)
        },
        setCameras (state, cameras) {
            state.cameras = cameras
        },
        setRooms (state, rooms) {
            state.rooms = rooms
        },
        setRoom (state, room) {
            state.rooms.push(room)
        },
        setSector (state, sector) {
            state.sectors.push(sector)
        },
        setSectors (state, sectors) {
            state.sectors = sectors
        },
        setSectorTypes (state, sectorTypes) {
            state.sectorTypes = sectorTypes
        },
        setRoomTypes (state, roomTypes) {
            state.roomTypes = roomTypes
        },
        setTasks (state, tasks) {
            state.tasks = tasks
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
            commit('setCamera', newCamera)
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
        async getSectorsByCameraIDFromDB({commit}, id) {
            let returnResult
            try {
                returnResult = await fetch(`http://localhost:5000/getSectorsByCameraID?id=${id}`, {
                    credentials: "include",
                    method: 'GET',
                    cors: 'no-cors',
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8',
                    },
                })
                    .then(response => response.json())
                    .then((response) => {
                        console.log('sectors ')
                        console.log(response)
                        commit('setSectors', response)
                        return Promise.resolve('ok')
                    });
            } catch (err) {
                console.log(err)
            }
            return returnResult
        },
        async getSectorTypesFromDB({commit}) {
            let returnResult
            try{
                returnResult = await fetch(`http://localhost:5000/getSectorTypes`, {
                    credentials: "include",
                    method: 'GET',
                    cors: 'no-cors',
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8',
                    },
                })
                    .then(response => response.json())
                    .then((response) => {
                        returnResult = response
                        console.log('sectorTypes')
                        commit('setSectorTypes', response)
                        return response
                        // console.log(this.$store.state.sectorTypes)
                    });
            } catch (err) {
                console.log(err)
            }
            return returnResult
        },
        async getRoomTypesFromDB({commit}) {
            let returnResult
            try{
                returnResult = await fetch(`http://localhost:5000/getRoomTypes`, {
                    credentials: "include",
                    method: 'GET',
                    cors: 'no-cors',
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8',
                    },
                })
                    .then(response => response.json())
                    .then((response) => {
                        returnResult = response
                        console.log('roomTypes')
                        commit('setRoomTypes', response.types)
                        return response
                    });
            } catch (err) {
                console.log(err)
            }
            return returnResult
        },
        async getRoomsFromDB({commit}) {
            let returnResult
            try{
                returnResult = await fetch('http://localhost:5000/getRooms', {
                    credentials: "include",
                    method: 'GET',
                    cors: 'no-cors',
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8',
                    },
                })
                    .then(response => response.json())
                    .then((response) => {
                        returnResult = response
                        console.log('getRoomsFromDB ' + response)
                        commit('setRooms', response)
                        return response
                    });
            } catch (err){
                console.log(err)
            }
            return returnResult
        },
        async getCamerasFromDB({commit}) {
            let returnResult
            try{
                returnResult = await fetch('http://localhost:5000/getCameras', {
                    credentials: "include",
                    method: 'GET',
                    cors: 'no-cors',
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8',
                    },
                })
                    .then(response => response.json())
                    .then((response) => {
                        returnResult = response
                        commit('setCameras', response)
                        return response
                        // this.$store.state.cameras = response
                    });
            } catch (err) {
                console.log(err)
            }
            return returnResult
        },
        async getTasksFromDB({commit}, selectedDay){
            let returnResult
            try{
                returnResult = await fetch('http://localhost:5000/getTasks', {
                    credentials: "include",
                    method: 'POST',
                    // cors: 'no-cors',
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8',
                    },
                    body: JSON.stringify({
                        "date": selectedDay
                    })
                })
                    .then(response => response.json())
                    .then((response) => {
                        returnResult = response
                        // console.log(this.selectedDay)
                        console.log('getTasksFromDB')
                        commit('setTasks', response)
                        return response
                        // console.log(this.randomHex())
                    });
            } catch (err){
                console.log(err)
            }
            return returnResult
        },
        addRoom({commit}, newRoom) {
            commit('setRoom', newRoom)
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
        getRoomTypes(state) {
            return state.roomTypes
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
        getAuthorized(state) {
            return state.authorized
        }
    },
})

