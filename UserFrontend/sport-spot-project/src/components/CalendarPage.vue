<template>
  <div>
    <div class="container" @mouseup="onMousedown=false">
      <div class="row justify-content-around">
      <div class="col-6">
        <label class="field">Календарь</label>
      </div>
        <div class="col-6">
          <label v-if="!roomSelected" class="field">Помещения</label>
          <label v-if="roomSelected" class="field">
            Помещение 1 {{`${this.selectedDay.substr(3, 2)}/${this.selectedDay.substr(0, 2)}/${this.selectedDay.substr(6, 4)}`}}
          </label>
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
                <button @click="getCurrentDay" class="hidden-button" title="К текущему месяцу">
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
<!--              <div class="calendar-number">1</div>-->
            </div>
          </div>
        </div>
      </div>
      <div class="col-6" >
        <div class="col-12 window window-onPage">
          <div v-if="selectedDay.length !== 0" class="row">
            <div v-if="!roomSelected" class="col-6">
              Занятые
            </div>
            <div v-if="!roomSelected" class="col-6">
              Свободные
              <div class="row window camera col-12" @click="chooseRoom(room)" v-for="(room, index) in getRooms"
                   :key="index">
                <span class="name">{{room.name}}</span>
              </div>
            </div>
          </div>
          <div class="row" v-if="roomSelected">
            <div class="col-5">
              Расписание
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
                    <template v-if="2 * index < 49">
                      <td
                          :id="timesArray[2 * index]"
                          class="linear-table-td"
                          @mouseenter = "setIndices(2 * index)"
                          @mousedown = "indexSelected = 2 * index; onMousedown = true; setIndices(2 * index)">
                        {{timesArray[2 * index]}}
                      </td>
                      <td
                          :id="timesArray[2 * index + 1]"
                          class="linear-table-td"
                          @mouseenter="setIndices(2 * index + 1)"
                          @mousedown = "indexSelected = 2 * index + 1; onMousedown = true; setIndices(2 * index + 1)">
                        {{timesArray[2 * index + 1]}}
                      </td>
                    </template>
                  </tr>
                </table>
              </div>
            </div>
            <div class="col-7">
              <div class="grid-default">
                Мероприятие
                <button class="hidden-button content content-end" @click="resetTask">
                  <img src="../assets/icons/add24.png" alt="">
                </button>
              </div>
              <form @submit.prevent="selectFunction(save)" style="margin-top: 10px">
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
                  <input class="input-field" type="text" v-model.trim="task.targetCount"
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
                <div style="width: 100%; margin-bottom: 10px">
                  <button type="submit" class="btn btn-success" >Сохранить</button>
                </div>
              </form>
              <button
                  v-if="taskSelected"
                  @click="clearTimesArray(this.task.timesArray); canChangeTimesArray = true"
                  class="btn btn-primary"
                  style="position: absolute; top: 0; right: 0; margin-right: 15px; margin-top: 132px">
                Выбрать время
              </button>
              Список мероприятий
                <div class="row" v-for="(task, index) in this.getTasks" :key="index">
                  <div class="window camera col-6" @click="chooseTask(task)">
                    <span class="name">{{task.name}}</span>
                    <span class="name" style="margin-left: 10px">0/{{task.targetCount}}</span>
                  </div>
                  <div class="col-2">
                    <input class="hidden-button"
                           type="color"
                           @change="repaintTimesArray(task.timesArray, task.color + alphaChannel); save(task)"
                           v-model.trim="task.color">
                  </div>
                  <div class="col-2">
                    <button class="hidden-button"
                            @click="removeTask(task.id); resetTask(); clearTimesArray(task.timesArray)">
                      <img src="../assets/icons/delete.png" alt="">
                    </button>
                  </div>
<!--                  <div class="col-2">-->
<!--                    <button-->
<!--                        title="Установить время"-->
<!--                        class="hidden-button"-->
<!--                        @click="clearTimesArray(task.timesArray)">-->
<!--                      <img src="../assets/icons/time.png" alt="">-->
<!--                    </button>-->
<!--                  </div>-->
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
import {mapGetters} from "vuex"
import {mapActions} from 'vuex'
import { useVuelidate } from '@vuelidate/core'
import {integer, required} from "@vuelidate/validators";

export default {
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
        timesArray: ''
      },
      // generatedColor: this.randomHex(),

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
      alphaChannel: '',
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
        'getRefreshInterval'
    ])
  },
  mounted() {
    if (this.getRefreshInterval){
      console.log('clean')
      this.$store.commit('clearRefreshInterval')
    }
    this.setCurrentDay()
    this.selectFunction(this.getRoomsFromDB)
    this.createTimesArray()
  },
  methods: {
    save(saveTask){
      let task = this.task
      if (arguments.length === 1) task = saveTask
      else this.v$.task.$touch()
      let returnResult
      console.log('save')
      if (new Date(this.selectedDay + ' ' + this.indexStart + ':00') < new Date()) alert("")
      else if(this.task.timesArray.length >= 2){
        if (!this.v$.task.$error) {
          fetch('http://localhost:5000/setTask', {
            credentials: "include",
            method: 'POST',
            cors: 'no-cors',
            headers: {
              'Content-Type': 'application/json;charset=utf-8',
            },
            body: JSON.stringify({
              "id": task.id,
              "name": task.name,
              "comment": task.comment,
              "roomId": this.roomSelectedId,
              "targetCount": task.targetCount,
              "begin": `${this.selectedDay} ${task.timesArray[0]}:00`,
              "end": `${this.selectedDay} ${task.timesArray[task.timesArray.length-1]}:00`,
              "color": task.color
            })
          })
              .then(response => response.json())
              .then((response) => {
                console.log(response)
                returnResult = response
                this.task.id = response.id
                if (this.getTaskByID(this.task.id) === undefined)
                  this.$store.commit('setTask', Object.assign({}, this.task))
                this.repaintTimesArray(task.timesArray, task.color + this.alphaChannel).then((value => {
                      console.log(value)
                      this.resetTask()
                    })
                )
                // this.resetTask().then((value) =>{
                //       console.log(value)
                //       this.paintTimesArray(task.timesArray)
                //     }
                // )
              });
        }
      }
      else alert("Выберите диапазон времени более одного значения")
      return returnResult
    },
    getRoomsFromDB() {
      let returnResult
      fetch('http://localhost:5000/getRooms', {
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
            console.log('resp ' + response)
            this.$store.state.rooms = response
          });
      // console.log(returnResult)
      return returnResult
    },
    getTasksFromDB(){
      let returnResult
      fetch('http://localhost:5000/getTasks', {
        credentials: "include",
        method: 'POST',
        // cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
        body: JSON.stringify({
          "date": this.selectedDay
        })
      })
          .then(response => response.json())
          .then((response) => {
            returnResult = response
            console.log(this.selectedDay)
            console.log(response)
            this.$store.state.tasks = response
            console.log(this.randomHex())
            for (let task of this.getTasks){
              let indexStart = this.getTimeIndex(task.begin)
              let indexEnd = this.getTimeIndex(task.end)
              task.timesArray = this.$data.timesArray.slice(indexStart, indexEnd+1)
              // console.log('sliceArray ' + indexStart, indexEnd)
              // let color = this.randomHex()
              // task.color = color.slice(0, 7)
              this.paintTimesArray(task.timesArray, task.color + this.alphaChannel)
              for (let time of task.timesArray){
                this.busyTimesArray.push(time)
              }
            }
          });
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
      this.indexEnd = ''
      this.indexStart = ''
      this.canChangeTimesArray = true
      this.paintTimesArray(this.task.timesArray, '#ffffff66')
      return 0
    },
    getTimeIndex(time){
      let getTime = new Date(time)
      let date = `${getTime.getHours().toString().length === 1 ? "0" : ""}${getTime.getHours()}:${getTime.getMinutes().toString().length === 1 ? "0" : ""}${getTime.getMinutes()}`
      // console.log('date ' + date)
      return this.timesArray.indexOf(date)
    },
    randomHex(){
      this.alphaChannel = Math.round(0.4 * 255).toString(16)
      let color = Math.floor(Math.random()*16777215).toString(16)
      color = color.length === 6 ? color : color + "0"
      console.log('a: ' + this.alphaChannel + " " + color)
      return `#${color}${this.alphaChannel}`
    },
    setIndices(index){
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
      let sliceArray = this.$data.timesArray.slice(indexStart, indexEnd+1)
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
            this.setBusyTimeArray(timesArray).then((value => {
                  console.log(value)
                  this.task.timesArray = []
                })
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
          if (sliceArray.includes(i)){
            // console.log('include ' + i)
            document.getElementById(i).style.setProperty('--color', color)
            document.getElementById(i).classList.add('linear-table-td-painted')
            // document.getElementById(i).classList.add(`task-${}`)
          }
          else {
            document.getElementById(i).classList.remove('linear-table-td-painted')
          }
          this.indexStart = sliceArray[0]
          this.indexEnd = sliceArray[sliceArray.length-1]

          this.task.timesArray = sliceArray
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
      for (let time of timesArray){
        this.busyTimesArray.push(time)
      }
      return 'setBusyTimeArray'
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
      if (this.selectedDay !== '') this.chooseDay(day, (parseInt(day) - 1).toString())

    },
    chooseDay(day, index){
      if (index >= this.days.length){
        index = (this.days[this.days.length-2])
        day = index + 1
      }
      let monthStr = this.currentMonth + 1
      if (day.toString().length !== 2) day = `0${day}`
      if (monthStr.toString().length !== 2) monthStr = `0${monthStr}`
      this.selectedDay = `${monthStr}/${day}/${this.currentYear}`

      console.log(index + ' ' + this.prevCalendarIndex)

      document.getElementById(index).classList.add('calendar-number-selected')
      document.getElementById(index).style.color = 'aliceblue'
      if (this.prevCalendarIndex !== null && this.prevCalendarIndex !== index)
        if (document.getElementById(this.prevCalendarIndex).classList.length !== 0){
          console.log('remove')
          document.getElementById(this.prevCalendarIndex).classList.remove('calendar-number-selected')
          document.getElementById(this.prevCalendarIndex).style.color = ''
        }

      this.prevCalendarIndex = index

      if (this.roomSelected){
        this.resetTask()
        this.busyTimesArray = []
        for (let i of this.timesArray) document.getElementById(i).classList.remove('linear-table-td-painted')
        this.selectFunction(this.getTasksFromDB)
      }
    },
    chooseRoom(room){
      this.roomSelected = true
      this.roomSelectedId = room.id
      console.log(this.selectedDay)
      console.log(room)
      this.selectFunction(this.getTasksFromDB)
    },
    setCurrentDay(){
      this.setCorrectMonth().then((value => {
            console.log(value)
            let date = new Date()
            if (this.currentMonth === date.getMonth() && this.currentYear === date.getFullYear())
              document.getElementById((date.getDate() - 1).toString()).classList.add('calendar-number-current')
            else document.getElementById((date.getDate() - 1).toString()).classList.remove('calendar-number-current')
          })
      )
    },
    getCurrentDay(){
      let curDay = new Date()
      this.currentMonth = curDay.getMonth()
      this.currentYear = curDay.getFullYear()
      this.setCurrentDay()

      let day = this.selectedDay.substr(3, 2)
      console.log(this.selectedDay)
      this.prevCalendarIndex = null
      if (this.selectedDay !== '') this.chooseDay(day, (parseInt(day) - 1).toString())
    },
    async setCorrectMonth(){
      let curDay = new Date()
      curDay.get
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
      // console.log(this.timesArray)
    },
    selectFunction(func){
      let respFunc = func()
      let refresh
      console.log('respFunc ' + respFunc)
      if (respFunc === "Bad token") {
        refresh = this.refreshToken()
        if (refresh === "ok"){
          console.log('refreshOk')
          respFunc = func()
        }
        if (respFunc === "Bad token") alert('logout pls')
      }
      else return "ok"
    },
    ...mapActions([
        'removeTask',
        'refreshToken'
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
  background-size: 100% 37px;
  &-td{
    font-size: 11px;
    &:hover{
      cursor: pointer;
    }
    &-painted {
      background-color: var(--color) ;
    //rgba(255, 230, 0, 0.25)
    }
  }
}
.scroll-table{
  height: 480px;
  overflow-x: auto;
  margin-top: 5px;
}
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
}
</style>