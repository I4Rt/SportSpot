// import { createApp } from 'vue'
import { createStore } from 'vuex'
// import axios from "axios";

export default createStore({
    state () {
        return {
            cameraCount: 0,
            roomCount: 0,
            cameras: [],
            rooms: [],
            sectorTypes: ['ПОЛ', 'ЗЕРКАЛО']
        }
    },
    mutations: {
        setCameras (state, camera) {
            state.cameras.push(camera)
        },
        setRooms (state, room) {
            state.rooms.push(room)
        },
        setCameraCount (state, cameraCount) {
            state.cameraCount = cameraCount
        },
        setRoomCount (state, roomCount) {
            state.roomCount = roomCount
        }
    },
    actions: {
        addCamera({commit}, newCamera) {
            commit('setCameras', newCamera)
        },
        addRoom({commit}, newRoom) {
            commit('setRooms', newRoom)
        },
        addCameraCount({commit}, cameraCount) {
            commit('setCameraCount', cameraCount)
        },
        addRoomCount({commit}, roomCount) {
            commit('setRoomCount', roomCount)
        }
    },
    getters: {
        getCameras(state) {
            return state.cameras
        },
        getCameraByID: (state) => (id) => {
            return state.cameras.find(camera => camera.id === id)
        },
        getCamerasByRoomID: (state) => (id) => {
          return state.cameras.filter(camera => camera.roomID === id)
        },
        getCamerasWithoutRoomID (state) {
            return state.cameras.filter(camera => camera.roomID === -1)
        },
        getRooms(state) {
            return state.rooms
        },
        getRoomByID: (state) => (id) => {
            return state.rooms.find(room => room.id === id)
        },
        getSectorTypes(state) {
            return state.sectorTypes
        },
        getCameraCount(state) {
            return state.cameraCount
        },
        getRoomCount(state) {
            return state.roomCount
        }
    }
})

