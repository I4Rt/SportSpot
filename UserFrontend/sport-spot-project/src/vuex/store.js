// import { createApp } from 'vue'
import {createStore} from 'vuex'
// import axios from "axios";

export default createStore({
    state () {
        return {
            file: null,
            files: [],
            tasks: [],
            cameras: null,
            rooms: [],
            sector: null,
            sectors: null,
            sectorTypes: [],
            roomTypes: [],
            unusedCameras: {},
            usedCameras: {},
            refreshInterval: null,
            archiveInterval: null,
            authorized: false,
            user: {}
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
        addSector (state, sector) {
            state.sectors.push(sector)
        },
        deleteSector (state, index) {
          state.sectors.splice(index, 1)
        },
        setSector (state, sector) {
            state.sector = sector
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
        setFile (state, file) {
            state.file = file
        },
        setFiles (state, files) {
            state.files = files
        },
        setUser (state, user) {
            state.user = user
        },
        setRefreshInterval (state, interval) {
          state.refreshInterval = interval
        },
        clearRefreshInterval (state) {
            clearInterval(state.refreshInterval)
            state.refreshInterval = null
        },
        setArchiveInterval (state, interval) {
            state.archiveInterval = interval
        },
        clearArchiveInterval (state) {
            clearInterval(state.archiveInterval)
            state.archiveInterval = null
        }
    },
    actions: {
        addCamera({commit}, newCamera) {
            commit('setCamera', newCamera)
        },
        async removeCamera({commit}, id) {
            let returnResult
            try{
                console.log('remove')
                returnResult =  await fetch(`http://localhost:5000/removeCamera?id=${id}`, {
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
                        return response
                    })
            } catch (err){
                console.log(err)
            }
            return returnResult
        },
        async removeRoom({commit}, id) {
            let returnResult
            try{
                returnResult = await fetch(`http://localhost:5000/removeRoom?id=${id}`, {
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
                        return response
                    })
            } catch (err){
                console.log(err)
            }
            return returnResult

        },
        async removeTask({commit}, id) {
            let returnResult
            try{
                returnResult = await fetch(`http://localhost:5000/removeTask?id=${id}`, {
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
                        return response
                    })
            } catch (err) {
                console.log(err)
            }
            return returnResult
        },
        async removeSector({commit}, id) {
            let returnResult
            try{
                returnResult = await fetch(`http://localhost:5000/removeSector?id=${id}`, {
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
            } catch (err) {
                console.log(err)
            }
            return returnResult
        },
        async setSectorToDB({commit}, sector) {
            console.log('setSectorToDB')
            let returnValue
            try {
                returnValue = await fetch('http://localhost:5000/setSector', {
                    credentials: "include",
                    method: 'POST',
                    cors: 'no-cors',
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8',
                    },
                    body: JSON.stringify({
                        "camId": sector.camId,
                        "id": sector.id,
                        "name": sector.name,
                        "points": sector.points,
                        "roomId": sector.roomId,
                        "typeId": sector.typeId
                    })
                })
                    .then(response => response.json())
                    .then((response) =>{
                        sector.id = response.id
                        if (sector.id === null) return response
                        else{
                            if (this.state.sector === null) commit('setSector', sector)
                            return sector
                        }
                    })
            } catch (err) {
                console.log(err)
            }
            return returnValue
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
        async getRoomsForDayFromDB({commit}, selectedDay){
            console.log('getRoomsForDay')
            let returnResult
            try{
                returnResult = await fetch(`http://localhost:5000/getRoomsForDay`, {
                    credentials: "include",
                    method: 'POST',
                    cors: 'no-cors',
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8',
                    },
                    body: JSON.stringify({
                        'date': selectedDay
                    })
                })
                    .then(response => response.json())
                    .then((response) => {
                        console.log(response)
                        try {
                            if (!response.answer) commit('setRooms', response)
                        } catch (err) {
                            console.log(err)
                        }
                        return response
                    })
            } catch (err) {
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
        async getByRoutes({commit}, data) {
            console.log(data)
            let returnResult
            try{
                returnResult = await fetch(`http://localhost:5000/getByRoutes`, {
                    credentials: "include",
                    method: 'POST',
                    cors: 'no-cors',
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8',
                    },
                    body: JSON.stringify(data)
                })
                    .then(response => response.json())
                    .then((response) => {
                        returnResult = response
                        console.log('getByRoutes')
                        console.log(response)
                        try {
                            if (response.answer === 'can not open file'){
                                alert('Неподдерживаемый тип файла, выберите другой')
                            }
                            else if (response.folderData)
                                commit('setFiles', response.folderData)
                        } catch (err){
                            console.log(err)
                        }
                        return response
                    });
            } catch (err) {
                if (err instanceof TypeError) alert('Искомый путь не найден')
            }
            return returnResult
        },
        async getUserInfoFromDB({commit}) {
            let returnResult
            try{
                returnResult = await fetch('http://localhost:5000/getUserInfo', {
                    credentials: "include",
                    method: 'GET',
                    // cors: 'no-cors',
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8',
                    }
                })
                    .then(response => response.json())
                    .then((response) => {
                        returnResult = response
                        // console.log(this.selectedDay)
                        console.log('getUserInfo')
                        commit('setUser', response)
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
        getArchiveInterval(state){
            return state.archiveInterval
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
            if (state.sectors === null) return state.sectors
            else return state.sectors.filter(sector => sector.camId === id)
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
        getFiles(state) {
            return state.files
        },
        getFilesByDay: (state) => (date) => {
            console.log('day')
            return state.files.filter(file => {
                if (!file.createTime) return true

                let fileDate = new Date(file.createTime.substring(0, file.createTime.length-4))
                let fullFileDate = new Date(`${fileDate.getFullYear()}-${fileDate.getMonth()+1}-${fileDate.getDate()}`).getTime()

                let fullDate = date.getTime()-(7*60*60*1000)
                // console.log(`${fullFileDate === fullDate}  ${new Date(fullFileDate)}  ${new Date(fullDate)}`)
                return fullFileDate === fullDate
            })
        },
        getFilesByName: (state) => (name) => {
            console.log('name')
            return state.files.filter(file => file.name.toLowerCase().includes(name.toLowerCase()))
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
        getTasksByRoomID: (state) => (roomId) => {
            return state.tasks.filter(task => task.roomId === roomId)
        },
        getAuthorized(state) {
            return state.authorized
        },
        getFile(state) {
            return state.file
        },
        getUser(state) {
            return state.user
        },
    },
})

