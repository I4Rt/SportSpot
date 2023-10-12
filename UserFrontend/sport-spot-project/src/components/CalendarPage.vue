<template>
    <div class="container" @mouseup="onMousedown=false">
      <div class="row justify-content-around">
      <div class="col-6">
        <label class="field">Календарь</label>
      </div>
        <div class="col-6">
          <div class="grid-default" :class="roomSelected ? 'grid-default-room-label' : ''">
            <div class="content content-start">
              <label v-if="!roomSelected" class="field">Помещения</label>
              <div v-if="roomSelected" class="grid-default grid-default-room-label" style="margin-left: 5px">
                <label
                    class="field short-name short-name-room-label"
                    :title="getRoomByID(roomSelectedId).name">
                  {{getRoomByID(roomSelectedId).name}}
                </label>
                <div class="content content-start">
                  <label class="field">
                    {{`${selectedDay.substr(3, 2)}/${selectedDay.substr(0, 2)}/${selectedDay.substr(6, 4)}`}}
                  </label>
                </div>

              </div>
            </div>
            <div class="content content-end">
              <button v-if="roomSelected"
                      class="btn btn-primary"
                      style="margin-right: 5px; padding: 3px 8px"
                      @click="roomSelected = false; busyTimesArray = []; selectFunction(getRoomsForDayFromDB, selectedDay)">Назад</button>
              <label v-if="getFile !== null" class="field">Выбран архивный файл</label>
            </div>
          </div>
        </div>
      <div class="col-6 " >
        <div class="col-12 window window-onPage" style="display: flow-root">
          <div  class="calendar window">
            <div class="calendar-month">
              <div class="calendar-month-el">
                <button @click="chooseMonth('back')" class="hidden-button content content-center">
                  <img  :src="require('../assets/icons/back.png')" alt="">
                </button>
                <button @click="chooseMonth('next')" class="hidden-button content content-center" >
                  <img  :src="require('../assets/icons/next.png')" alt="">
                </button>
                <div class="content content-center"> {{calendarMonths[currentMonth]}} </div>
                <div class="content content-start"> {{currentYear}} </div>
                <button @click="getCurrentDay" class="hidden-button" title="К текущему дню">
                  <img  :src="require('../assets/icons/today24px.png')" alt="">
                </button>
              </div>
            </div>
            <div class="calendar-date">
              <div
                  class="calendar-day"
                  v-for="(calendarDay, index) in calendarDays"
                  :key="index">
                {{calendarDay}}
              </div>
              <div class="calendar-number" v-for="(index) in missedDays" :key="index"></div>
              <div
                  @click="chooseDay(day, index)"
                  class="calendar-number"
                  v-for="(day, index) in days"
                  :key="index"
                  :id="index">
                {{day}}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-6" >
        <div class="col-12 window window-onPage">
          <div style="text-align: center" v-if="selectedDay.length === 0">
            <img :src="require('../assets/gifs/black-spinner.svg')" style="width: 100px; height: 100px" alt="">
          </div>
          <div v-else-if="!roomSelected" class="row">
            <div class="col-12">
              <div class="row window camera col-12" @click="chooseRoom(room)" v-for="(room, index) in getRooms"
                   :key="index" style="margin-top: 10px; margin-left: 0; padding-bottom: 10px">
                <span class="name short-name short-name-room" :title="room.name">{{room.name}}</span>
                <div style="width: 100%" class="grid-default grid-default-squares">
                  <div v-for="(square, index) in room.selectedTime" :key="index"
                       style="width: 10px; height: 10px; border: 1px solid black"
                       :style="square === 0 ? {'background-color': 'white'} : {'background-color': 'greenyellow'}">
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row" v-else>
            <div class="col-5">
              <div class="window">
                <table
                    class="linear-table window-table"
                    style="width: 100%"
                    @mousedown="onMousedown=true">
                  <tr
                      v-for="(time, index) in timesArray"
                      :key="index"
                      onmousedown="return false"
                      onselect="return false">
                    <template v-if="2 * index < 48">
                      <td
                          :id="timesArray[2 * index]"
                          class="linear-table-td"
                          @mouseenter = "setIndices(2 * index)"
                          @mousedown = "indexSelected = 2 * index; onMousedown = true; setIndices(2 * index)">
                        {{timesArray[2 * index]}} - {{timesArray[2 * index + 1]}}
                      </td>
                      <td
                          :id="timesArray[2 * index + 1]"
                          class="linear-table-td"
                          @mouseenter="setIndices(2 * index + 1)"
                          @mousedown = "indexSelected = 2 * index + 1; onMousedown = true; setIndices(2 * index + 1)">
                        <span >
                          {{timesArray[2 * index + 1]}} - {{timesArray[2 * index + 1] === '23:30' ? '24:00' : timesArray[2 * index + 2]}}
                        </span>

                      </td>
                    </template>
                  </tr>
                </table>
              </div>
            </div>
            <div class="col-7">
                <div  class="grid-default grid-default-task-label"  v-if="getFile !== null">
                  <span
                      class="short-name"
                      :title="getFile.name">
                    Архивный файл <br>
                    <span
                        style="font-size: 17px; font-weight: 700; "
                        class="short-name">
                      {{getFile.name}}
                    </span>
                  </span>
                  <div class="content content-end">
                    <button style="padding: 2px 8px" class="btn btn-danger" @click="$store.state.file = null">Х</button>
                  </div>
                </div>
                <div style="margin-bottom: 5px" v-else class="grid-default grid-default-task-label">
                  <label>Задать мероприятие</label>
                  <button
                      title="Создать новое мероприятие"
                      class="hidden-button content content-end" @click="resetTask">
                    <img src="../assets/icons/add24.png" alt="">
                  </button>
                </div>
              <form @submit.prevent="selectFunction(save)" >
                <div class="">
                  <label> Название: </label>
                  <input class=" input-field" type="text" v-model.trim="task.name"
                         :class="v$.task.name.$error ? 'is-invalid' : ''">
                  <p v-if="v$.task.name.$dirty && v$.task.name.required.$invalid " class="invalid-feedback">
                    Обязательное поле
                  </p>
                </div>
                <div class="">
                  <label> Количество участников: </label>
                  <input class="input-field" type="number" v-model.trim="task.targetCount"
                         :class="v$.task.targetCount.$error ? 'is-invalid' : ''">
                  <p v-if="v$.task.targetCount.$dirty && v$.task.targetCount.required.$invalid " class="invalid-feedback">
                    Обязательное поле
                  </p>
                  <p v-if="v$.task.targetCount.$dirty && v$.task.targetCount.integer.$invalid " class="invalid-feedback">
                    Значение должно быть числовым
                  </p>
                </div>
                <div class="">
                  <label> Комментарий: </label>
                  <input class="input-field" type="text" v-model.trim="task.comment">
                </div>
                <div>
<!--                  <input v-model="duplicateTask" type="checkbox">-->
<!--                  <span style="font-size: 14px">  Сохранять мероприятие каждый день до:</span>-->
<!--                  <input v-model.trim="duplicateDate" type="date">-->
<!--                  <button @click="checkToDuplicate">Dupl</button>-->
                </div>
                <div style="width: 100%; margin-bottom: 10px; margin-top: 10px" class="grid-default">
                  <button type="submit" class="btn btn-success" >Сохранить</button>
                  <button
                      type="button"
                      v-if="taskSelected"
                      @click="clearTimesArray(this.task.timesArray); canChangeTimesArray = true"
                      class="btn btn-primary">
                    Выбрать время
                  </button>
                </div>
              </form>
              Список мероприятий
                <div style="text-align: center" v-if="!tasksLoaded">
                  <img :src="require('../assets/gifs/black-spinner.svg')" style="width: 100px; height: 100px" alt="">
                </div>
                <div v-else class="scroll scroll-tasks">
                  <div
                      class="grid-default grid-default-tasks"
                      v-for="(selectedTask, index) in this.getTasksByRoomID(roomSelectedId)"
                      :key="index"
                      style="margin-left: 5px; margin-bottom: 5px">
                    <div  :style="task.id === selectedTask.id ? {background: '#a7a7a7'} : '' "
                          class="window camera grid-default grid-default-task-info"
                          @click="chooseTask(selectedTask)">
                      <span class="name short-name short-name-task" :title="selectedTask.name">{{selectedTask.name}}</span>
                      <span class="name content content-end" style="margin-left: 10px">{{selectedTask.statistics}}/{{selectedTask.targetCount}}</span>
                    </div>
                    <div class="">
                      <input class="hidden-button"
                             type="color"
                             @change="repaintTimesArray(selectedTask.timesArray, selectedTask.color + alphaChannel); save(selectedTask)"
                             v-model.trim="selectedTask.color" disabled>
                    </div>
                    <div class="">
                      <button class="hidden-button"
                              @click="removeTask(selectedTask.id); resetTask(); clearTimesArray(selectedTask.timesArray)">
                        <img src="../assets/icons/delete.png" alt="">
                      </button>
                    </div>
                  </div>
                </div>

            </div>
          </div>
        </div>
      </div>
      </div>
    </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex"
import {useVuelidate} from '@vuelidate/core'
import {integer, required} from "@vuelidate/validators";
// import explorerPage from "@/components/ExplorerPage";

export default {
  props: ['selectFunction'],
  emits: ['onLogout'],
  name: "CalendarPage",
  setup () {
    return {
      v$: useVuelidate()
    }
  },
  data() {
    return{
      task: {
        id: null,
        name: '',
        comment: '',
        roomId: null,
        targetCount: null,
        begin: '',
        end: '',
        color: this.randomHex().slice(0,7),
        timesArray: '',
        interval: 5,
        statistics: 0
      },
      duplicateTask: false,
      duplicateDate: '',

      tasksLoaded: false,

      openExplorer: false,
      routeToFile: null,

      indexStart: null,
      indexEnd: null,
      indexSelected: null,
      onMousedown: false,
      timesArray: [],
      busyTimesArray: [],

      roomSelected: false,
      taskSelected: false,
      roomSelectedId: null,

      canChangeTimesArray: true,

      prevCalendarIndex: null,
      selectedDay: '',
      daysCount: 32,
      alphaChannel: '66',
      currentMonth: new Date().getMonth(),
      currentYear: new Date().getFullYear(),
      calendarMonths30: [3, 5, 8, 10],
      calendarMonths31: [0, 2, 4, 6, 7, 9, 11],
      calendarMonths: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
      calendarDays: ['ПН','ВТ','СР','ЧТ','ПТ','СБ','ВС'],
      days: null,
      missedDays: null
    }
  },
  validations: {
    task: {
      name: {required},
      targetCount: {required, integer},
      timesArray: {required},
    }
  },
  computed: {
    ...mapGetters([
        'getRooms',
        'getTasks',
        'getTaskByID',
        'getTasksByRoomID',
        'getRefreshInterval',
        'getRoomByID',
        'getFile'
    ])
  },
  mounted() {
    if (this.getRefreshInterval){
      console.log('clean')
      this.$store.commit('clearRefreshInterval')
    }
    this.setCurrentDay()
    // this.selectFunction(this.getRoomsFromDB)
    this.createTimesArray()
  },
  methods: {
    async checkToDuplicate(task){
      let returnResult = true
      console.log('\ndupl')
        let date1 = new Date(this.selectedDay)
        let date2 = new Date(new Date(this.duplicateDate).getTime()- 7*60*60*1000)
        let dates = (date2 - date1)/86400000 // количество дней
      console.log('dupl ' + this.duplicateDate)
      console.log('dates ' + dates + ' ' + date1 + ' ' + new Date(date2))
        for (let i = 0; i < dates; i++){
          console.log('nextDay')
          console.log(date1)
          date1 = this.nextDay(date1)
          console.log(date1)
          let finalDate = this.getCorrectFormatDate(new Date(date1))
          console.log(finalDate)
          let resp = await this.setTaskToDB(task, finalDate)
          if (resp === 'error') returnResult = false
        }
        if (!this.taskSelected){
          this.paintTasks()
          this.resetTask()
        }
        if (!returnResult) alert('Мероприятия записались не полностью. Возможно, произошло наложение времени')
    },

    save(saveTask){
      let task = this.task
      if (arguments.length === 1) task = saveTask
      else this.v$.task.$touch()
      console.log('save')
      if (this.getFile !== null) {
        if (new Date(this.selectedDay + ' ' + this.indexStart + ':00') >= new Date()) alert("Нельзя задать дату и время после текущего")
        else if (this.duplicateDate){
          this.setTaskToDB(task, this.selectedDay).then(() => {
            this.checkToDuplicate(task)
          })
        }
        else {
          this.setTaskToDB(task, this.selectedDay).then(() => {
            if (!this.taskSelected){
              this.paintTasks()
              this.resetTask()
            }
          })
        }
      }
      else {
        if (new Date(this.selectedDay + ' ' + this.indexStart + ':00') < new Date()) alert("Нельзя задать дату и время до текущего")
        else if (this.duplicateDate) {
          this.setTaskToDB(task, this.selectedDay).then(() => {
            this.checkToDuplicate(task)
          })
        }
        else {
          this.setTaskToDB(task, this.selectedDay).then(() => {
            if (!this.taskSelected){
              this.paintTasks()
              this.resetTask()
            }
          })
        }
      }
    },

    async setTaskToDB(task, date) {
      let returnResult
      console.log('\nsetDate ' + date)

      if(task.timesArray.length >= 1){
        if (!this.v$.task.$error) {
          let request
          let dataBody = {
            "name": task.name,
            "comment": task.comment,
            "roomId": this.roomSelectedId,
            "targetCount": task.targetCount,
            "interval": task.interval,
            "begin": `${date} ${this.indexStart}:00`,
            "end": `${this.indexEnd === '00:00' ? this.nextDay(new Date(date)) : date} ${this.indexEnd}:00`,
            "color": task.color
          }
          if (this.getFile === null){
            request = 'setTask'
            dataBody["id"] = task.id
          }
          else{
            request = 'sendForAnalize'
            dataBody["route"] = this.getFile.route.replaceAll('\\', '/')
          }
          console.log(dataBody)

          try {
            returnResult = await fetch(`http://localhost:5000/${request}`, {
              credentials: "include",
              method: 'POST',
              cors: 'no-cors',
              headers: {
                'Content-Type': 'application/json;charset=utf-8',
              },
              body: JSON.stringify(dataBody)
            })
                .then(response => response.json())
                .then((response) => {
                  console.log(response)
                  try {
                    if (response.name){
                      if (this.task.id === null) this.task.id = response.id
                      if (this.getTaskByID(this.task.id) === undefined)
                        this.$store.commit('setTask', Object.assign({}, this.task))
                    }
                    else if (response.answer === 'recogonition beguns') alert ('Выбранный файл анализируется')
                    else{
                      response = 'error'
                      alert('Что-то пошло не так, попробуйте еще раз')
                      this.resetTask()
                    }
                    this.canChangeTimesArray = false
                    this.repaintTimesArray(task.timesArray, task.color + this.alphaChannel).then((value => {
                      // if (!this.taskSelected) this.taskSelected = ''
                      console.log(value)
                      if (date === this.selectedDay){
                        this.selectFunction(this.getTasksFromDB, this.selectedDay).then(() => {
                          this.$store.state.file = null
                        })
                      }
                        })
                    )
                  } catch (err) {
                    console.log(err)
                  }
                  return response
                });
          } catch (err) {
            console.log(err)
          }
        }
      }
      else alert("Выберите диапазон времени")
      return returnResult
    },

    chooseTask(task) {
      console.log('choose')
      // this.resetTask()
      this.canChangeTimesArray = false
      this.task = task
      this.taskSelected = true
      this.paintTimesArray(this.task.timesArray, this.task.color + this.alphaChannel)
    },
    async resetTask() {
      let taskCopy = Object.assign({}, this.task)
      this.task = taskCopy
      this.task.id = null
      this.task.name = ''
      this.task.comment = ''
      this.task.roomId = this.roomSelectedId
      this.task.targetCount = null
      this.task.begin = ''
      this.task.end = ''
      this.task.color = this.randomHex().slice(0,7)
      this.task.timesArray = ''
      this.taskSelected = false
      this.v$.task.$reset()
      this.canChangeTimesArray = true
      this.paintTimesArray(this.task.timesArray, '#ffffff66')
      this.indexEnd = ''
      this.indexStart = ''
      this.duplicateTask = false
      this.duplicateDate = ''
      return 0
    },

    getTimeIndex(time){
      let getTime = new Date(time)
      let date = `${getTime.getHours().toString().length === 1 ? "0" : ""}${getTime.getHours()}:${getTime.getMinutes().toString().length === 1 ? "0" : ""}${getTime.getMinutes()}`
      // console.log('date ' + date)
      return this.timesArray.indexOf(date)
    },
    randomHex(){
      // this.alphaChannel = Math.round(0.4 * 255).toString(16)
      let color = Math.floor(Math.random()*16777215).toString(16)
      color = color.length === 6 ? color : color + "0"
      console.log('a: ' + this.alphaChannel + " " + color)
      return `#${color}${this.alphaChannel}`
    },
    setIndices(index){
      // console.log(`indexes: ${index}/${this.indexSelected}`)
      if (this.canChangeTimesArray === false) return 1
      let indexStart = null
      let indexEnd = null
      if (index < this.indexSelected) {
        indexEnd = this.$data.indexSelected
        indexStart = index
      }
      else {
        indexStart = this.indexSelected
        indexEnd = index
      }
      // console.log(`start/end: ${indexStart}/${indexEnd}`)
      let sliceArray = this.$data.timesArray.slice(indexStart, indexEnd+1)
      // console.log(sliceArray)
      let includesBusyTime = false
      for (let time of sliceArray) {
        if (this.busyTimesArray.includes(time)) includesBusyTime = true
      }
      if (this.onMousedown === true && !includesBusyTime) this.paintTimesArray(sliceArray)
    },
    async repaintTimesArray(timesArray, color){
      this.clearTimesArray(timesArray)
      this.paintTimesArray(timesArray, color).then((value => {
        console.log(value)
            this.setBusyTimeArray(timesArray).then((value) => {
              console.log('clearTimesArray')
                  console.log(value)
                  this.task.timesArray = []
              console.log('timesArray')
              console.log(this.task.timesArray)
                }
            )
      })
      )
      return 'repaintTimesArray'
    },
    async paintTimesArray(sliceArray, selectedColor){
      console.log('newPaint')
      let color = this.task.color + this.alphaChannel
      // console.log(color)
      if (arguments.length === 2) color = selectedColor
      else this.task.color = color.slice(0,7)
      for (let i of this.timesArray){
        if (!this.busyTimesArray.includes(i)){
          try {
            if (sliceArray.includes(i)){
              // console.log(sliceArray)
              // console.log('include ' + i)
              document.getElementById(i).style.setProperty('--color', color)
              document.getElementById(i).classList.add('linear-table-td-painted')
              // document.getElementById(i).classList.add(`task-${}`)
            }
            else {
              document.getElementById(i).classList.remove('linear-table-td-painted')
            }
            if (this.canChangeTimesArray) {
              this.indexStart = sliceArray[0]
              // sliceArray[sliceArray.length-1]
              let endIndex = this.timesArray.indexOf(
                  this.timesArray.find(el => el === sliceArray[sliceArray.length-1]))
              this.indexEnd = this.timesArray[endIndex] === '23:30' ? '00:00' : this.timesArray[endIndex+1]
            }
            this.task.timesArray = sliceArray //!!
          } catch (err) {
            console.log(err)
          }
        }
      }
      return 'paintTimesArray'
    },
    clearTimesArray(timesArray){
      for (let i of timesArray){
        if (this.busyTimesArray.includes(i))
          this.busyTimesArray = this.busyTimesArray.filter((time) => time !== i)
        document.getElementById(i).classList.remove('linear-table-td-painted')
      }
    },
    async setBusyTimeArray(timesArray){
      new Promise((resolve) => {
        for (let time of timesArray){
          this.busyTimesArray.push(time)
        }
        console.log('setBusyTimeArray')
        resolve('ok')
      })
    },
    chooseMonth(value){
      if (value === 'back'){
        if (this.currentMonth === 0) {
          this.currentMonth = 11
          this.currentYear -=1
        }
        else this.currentMonth -=1
      }
      else if (value === 'next'){
        if (this.currentMonth === 11) {
          this.currentMonth = 0
          this.currentYear +=1
        }
        else this.currentMonth +=1
      }
      this.setCurrentDay()

      let day = this.selectedDay.substr(3, 2)
      console.log(this.selectedDay)
      this.prevCalendarIndex = null
      console.log('selectedDay: ' + this.selectedDay)
      if (this.selectedDay !== '') this.chooseDay(day, (parseInt(day) - 1).toString())
    },
    nextDay(thisDay) {
      if (typeof thisDay === "string") thisDay = new Date(new Date(thisDay)-7*60*60*1000)
      console.log('value ' + thisDay)
      console.log('indexEnd ' + this.indexEnd)
      thisDay.setDate(thisDay.getDate() + 1)

      let monthStr = thisDay.getMonth() + 1
      let day = thisDay.getDate()
      if (day.toString().length !== 2) day = `0${day}`
      if (monthStr.toString().length !== 2) monthStr = `0${monthStr}`
      console.log('endValue\n')
      return `${monthStr}/${day}/${thisDay.getFullYear()}`
    },
    getCorrectFormatDate(date){
      console.log('correct Format')
      console.log(date)
      let day = date.getDate()
      let monthStr = date.getMonth() + 1
      if (day.toString().length !== 2) day = `0${day}`
      if (monthStr.toString().length !== 2) monthStr = `0${monthStr}`
      return `${monthStr}/${day}/${date.getFullYear()}`
    },
    chooseDay(day, index){
      console.log(`\nchooseDay ${day} ${index}`)
      if (index >= this.days.length){
        index = (this.days[this.days.length-2])
        day = index + 1
      }
      this.selectedDay = this.getCorrectFormatDate(new Date(`${this.currentMonth+1}-${day}-${this.currentYear}`))

      console.log(index + ' ' + this.prevCalendarIndex)

      document.getElementById(index).classList.add('calendar-number-selected')
      document.getElementById(index).style.color = 'aliceblue'

      if (this.prevCalendarIndex !== null && this.prevCalendarIndex !== index) {
        // if (document.getElementById(this.prevCalendarIndex).classList.length !== 0){
          console.log('remove')
          document.getElementById(this.prevCalendarIndex).classList.remove('calendar-number-selected')
          document.getElementById(this.prevCalendarIndex).style.color = ''
        }

      this.prevCalendarIndex = index

      if (this.roomSelected){
        this.resetTask()
        this.busyTimesArray = []
        for (let i of this.timesArray) document.getElementById(i).classList.remove('linear-table-td-painted')
        this.tasksLoaded = false
        this.selectFunction(this.getTasksFromDB, this.selectedDay).then(() => {
          this.paintTasks()
        })
      }
      else (this.selectFunction(this.getRoomsForDayFromDB, this.selectedDay))
    },
    chooseRoom(room){
      this.roomSelected = true
      this.roomSelectedId = room.id
      console.log(this.selectedDay)
      console.log(room)
      this.tasksLoaded = false
      this.selectFunction(this.getTasksFromDB, this.selectedDay).then(() => {
        this.paintTasks()
      })
    },
    paintTasks() {
      this.tasksLoaded = true
      console.log(`roomSelected ${this.roomSelectedId}`)
      for (let task of this.getTasksByRoomID(this.roomSelectedId)){
        let indexStart = this.getTimeIndex(task.begin)
        let indexEnd = this.getTimeIndex(task.end)-1 // чтобы не занимать ячейку, не подходящую по id
        let sliceArray = this.$data.timesArray.slice(indexStart, indexEnd+1)
        task.timesArray = sliceArray.length === 0 ? ['23:30'] : sliceArray
        console.log('color ' + task.color)
        this.paintTimesArray(task.timesArray, task.color + this.alphaChannel)
        for (let time of task.timesArray){
          this.busyTimesArray.push(time)
        }
        if (!this.taskSelected) this.resetTask()
      }
    },
    setCurrentDay(){
      this.setCorrectMonth().then((value => {
            console.log(value)
            let date = new Date()
            if (this.currentMonth === date.getMonth() && this.currentYear === date.getFullYear()){
              document.getElementById((date.getDate() - 1).toString()).classList.add('calendar-number-current')
              if (this.selectedDay === "") this.chooseDay(date.getDate(), date.getDate()-1)
              this.selectFunction(this.getRoomsForDayFromDB, this.selectedDay).then(() => {
                // if (this.getRooms.length !== 0) this.chooseRoom(this.getRooms[0])
              })
            }
            else document.getElementById((date.getDate() - 1).toString()).classList.remove('calendar-number-current')
          })
      )
    },
    getCurrentDay(){
      let curDay = new Date()
      this.currentMonth = curDay.getMonth()
      this.currentYear = curDay.getFullYear()
      this.setCurrentDay()

      let day = curDay.getDate().toString()
      if (this.selectedDay !== '') this.chooseDay(day, (parseInt(day) - 1).toString())
    },
    async setCorrectMonth(){
      let curDay = new Date()
      curDay.setDate(1)
      curDay.setMonth(this.currentMonth)
      curDay.setFullYear(this.currentYear)
      let day = curDay.getDay()
      if (day === 0) this.missedDays = [...Array(6)]
      else  this.missedDays = [...Array(day-1)]

      if (this.calendarMonths30.includes(this.currentMonth)) this.daysCount = 31
      else if (this.calendarMonths31.includes(this.currentMonth)) this.daysCount = 32
      else if (this.currentYear%4 === 0) this.daysCount = 30
      else this.daysCount = 29
      this.days = [...Array(this.daysCount).keys()].slice(1)

      return 'setCorrectMonth'
    },
    createTimesArray(){
      for (let i = 0; i < 25; i++){
        let setTime = ""
        // let hourArray = []
        if (i.toString().length !== 2) setTime = "0"
        this.timesArray.push(`${setTime}${i}:00`)
        this.timesArray.push(`${setTime}${i}:30`)
        // this.timesArray.push(hourArray)
      }
      this.timesArray.pop()
      this.timesArray.pop()
      // console.log(this.timesArray)
    },
    ...mapActions([
        'removeTask',
        'getRoomsFromDB',
        'getTasksFromDB',
        'getRoomsForDayFromDB'
    ])
  }
}
</script>

<style scoped lang="scss">
.field {
  font-size: 22px;
  font-weight: 700;
}
.window{
  box-shadow: 0 3px 4px rgba(0,0,0,.25);
  border-radius: 10px ;
  &-table{
    border-radius: 5px ;
  }
  &-onPage{
    height: 550px;
  }
}
.calendar {
  height: 400px;
  margin-top: 10px;
  //margin-top: 10px;
  //position: relative;
  //width: 400px;
  background-color: #fff;
  box-sizing: border-box;
  overflow: hidden;
}
.calendar-month{
  padding: 10px 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.grid-default{
  display: grid;
  grid-gap: 10px;
  grid-template-columns: 1fr 1fr;
  &-room-label{
    grid-template-columns: 60% 40%;
  }
  &-task-label{
    grid-template-columns: 1fr 50px;
  }
  &-squares{
    grid-template-columns: repeat(48, 1fr);
    grid-gap: 0;
  }
  &-tasks{
    grid-template-columns: 60% 20% 10%;
  }
  &-task-info{
    grid-template-columns: 70% 20%;
    grid-gap: 5px;
  }
}
.calendar-month-el{
  display: grid;
  grid-gap: 10px;
  grid-template-columns: 1fr 1fr 90px 50px 1fr;
  font-size: 19px;
  font-weight: 500;
}
.calendar-date {
  padding: 0 20px 20px;
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  grid-gap: 10px;
  box-sizing: border-box;
}
.calendar-day {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 25px;
  font-size: 16px;
  font-weight: 700;
  color: #262626;
  &:nth-child(7n){
    color: #ff685d;
  }
}
.calendar-number {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  font-size: 18px;
  font-weight: 400;
  color: #262626;
  border-radius: 5px;
  &-selected{
    font-weight: 700;
    background-color: #29239f;
    color: aliceblue;
  }
  &:hover{
    //background-color: #dadada;
    border: 2px solid #23b24e;
    cursor: pointer;
  }
  &:nth-child(7n){
    color: #ff685d;
  }
  &-current{
    color: #262626;
    font-weight: 700;
  }
}
.hidden-button{
  background: inherit;
  border: none;
  align-items: center;
  justify-content: center;
}
.content{
  display: flex;
  align-items: center;
  &-center{
    justify-content: center;
  }
  &-end{
    justify-content: end;
  }
  &-start{
    justify-content: start;
  }
}
.name{
  font-size: 14px;
  font-weight: 500;
  margin: 7px;
}
.camera:hover{
  background-color: #dadada;
  cursor: pointer;
}
.linear-table{
  background: linear-gradient(rgba(223, 224, 255, 0.5) 50%, #ffffff 50%);
  background-size: 100% 43px;
  &-td{
    width: 97px;
    font-size: 13px;
    &:hover{
      cursor: pointer;
    }
    &-painted {
      background-color: var(--color) ;
    //rgba(255, 230, 0, 0.25)
    }
  }
}
.scroll{
  overflow-y: auto;
  &-tasks{
    height: 250px;
  }
}
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb {
  box-shadow: inset 0 0 6px rgba(0,0,0,0.5);
  border-radius: 10px;
}
//.scroll-table{
//  height: 480px;
//  overflow-x: auto;
//  margin-top: 5px;
//}
.input-field{
  outline: none;
  width: 100px;
  height: 25px;
  font-size: 14px;
  position: absolute;
  right: 0;
  margin-right: 15px;
  border-radius: 5px ;
  border: 1px solid grey;
  &-file {
    margin-top: 10px;
    width: 300px;
    position: relative;
  }
}
.short-name {
  display: inline-block;
  width: 100%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  &-task {
   width: 80%;
  }
  &-room{
    width: 80%;
  }
  &-room-label{
    width: 100%;
  }
}

</style>