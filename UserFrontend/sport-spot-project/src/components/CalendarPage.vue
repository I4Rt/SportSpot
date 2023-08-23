<template>
  <div>
    <div class="container" @mouseup="onMousedown=false">
      <div class="row justify-content-around">
      <div class="col-6">
        <label class="field">Календарь</label>
      </div>
        <div class="col-6">
          <label v-if="!roomSelected" class="field">Помещения</label>
          <label v-if="roomSelected" class="field">Помещение 1 {{selectedDay}}</label>
        </div>
      <div class="col-6 " >
        <div class="col-12 window window-onPage" style="display: flow-root">
          <div  class="calendar window">
            <div class="calendar-month">
              <div class="calendar-month-el">
                <button @click="chooseMonth('back')" class="hidden-button">
                  <img  :src="require('../assets/icons/back.png')" alt="">
                </button>
                <button @click="chooseMonth('next')" class="hidden-button" >
                  <img  :src="require('../assets/icons/next.png')" alt="">
                </button>
                <div class="content content-center"> {{calendarMonths[currentMonth]}} </div>
                <div class="content content-start"> {{currentYear}} </div>
                <button @click="getCurrentDay" class="hidden-button" title="К сегодняшнему дню">
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
                  :class="[new Date().getDate() === day &&
                  currentMonth === new Date().getMonth() &&
                  currentYear === new Date().getFullYear() ? 'calendar-number-current' : '']"
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
                <span class="room-name">{{room.name}}</span>
              </div>
            </div>
          </div>
          <div class="row" v-if="roomSelected">
            <div class="col-5">
              Расписание
              <div class="window window-table">
                <table
                    class="linear-table"
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
                          @mouseenter = "paintTime(2 * index)"
                          @mousedown = "indexSelected = 2 * index; onMousedown = true; paintTime(2 * index)">
                        {{timesArray[2 * index]}}
                      </td>
                      <td
                          :id="timesArray[2 * index + 1]"
                          class="linear-table-td"
                          @mouseenter="paintTime(2 * index + 1)"
                          @mousedown = "indexSelected = 2 * index + 1; onMousedown = true; paintTime(2 * index + 1)">
                        {{timesArray[2 * index + 1]}}
                      </td>
                    </template>
                  </tr>
                </table>
              </div>
            </div>
            <div class="col-7">
              Мероприятие
              <form @submit.prevent="save" style="margin-top: 10px">
                <div class="">
                  <label> Название: </label>
                  <input class=" input-field" type="text" v-model.trim="task.name">
<!--                  <p v-if="v$.camera.name.$dirty && v$.camera.name.required.$invalid" class="invalid-feedback">-->
<!--                    Обязательное поле-->
<!--                  </p>-->
                </div>
                <div class="">
                  <label> Количество участников: </label>
                  <input class="input-field" type="text" v-model.trim="task.targetCount">
<!--                  <p v-if="v$.camera.ip.$dirty && v$.camera.ip.required.$invalid" class="invalid-feedback">-->
<!--                    Обязательное поле-->
<!--                  </p>-->
                </div>
                <div class="">
                  <label> Комментарий: </label>
                  <input class="input-field" type="text" v-model.trim="task.comment">
<!--                  <p v-if="v$.camera.chanel.$dirty && v$.camera.chanel.required.$invalid" class="invalid-feedback">-->
<!--                    Обязательное поле-->
<!--                  </p>-->
<!--                  <p v-if="v$.camera.chanel.$dirty && v$.camera.chanel.integer.$invalid " class="invalid-feedback">-->
<!--                    Канал должен быть числом-->
<!--                  </p>-->
                </div>
                <div style="width: 50px; margin-bottom: 10px">
                  <button type="submit" class="btn btn-success" >Сохранить</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "CalendarPage",
  data() {
    return{
      task: {
        id: null,
        name: '',
        comment: '',
        roomId: null,
        targetCount: null,
        begin: '',
        end: ''
      },
      indexStart: null,
      indexEnd: null,
      indexSelected: null,
      onMousedown: false,
      timesArray: [],

      roomSelected: false,
      roomSelectedId: null,

      prevCalendarIndex: null,
      selectedDay: '',
      daysCount: 32,
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
  computed: {
    ...mapGetters([
      'getRooms'
    ])
  },
  mounted() {
    this.setCorrectMonth()
    this.getRoomsFromDB()
    this.createTimesArray()
  },
  methods: {
    save(){
      console.log('save')
      fetch('http://192.168.169.32:5000/setTask', {
        method: 'POST',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
        body: JSON.stringify({
          "id": null,
          "name": this.task.name,
          "comment": this.task.comment,
          "roomId": this.roomSelectedId,
          "targetCount": this.task.targetCount,
          "begin": `${this.selectedDay} ${this.indexStart}:00`,
          "end": `${this.selectedDay} ${this.indexEnd}:00`,
        })
      })
          .then(response => response.json())
          .then((response) => {
            console.log(response)
            this.task.id = response.id
            this.$store.commit('setTask', Object.assign({}, this.room))
            // this.v$.room.$reset()
          });
    },
    getRoomsFromDB() {
      fetch('http://localhost:5000/getRooms', {
        method: 'GET',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
      })
          .then(response => response.json())
          .then((response) => {
            console.log(response)
            this.$store.state.rooms = response
          });
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
      this.setCorrectMonth()
    },
    chooseDay(day, index){
      let monthStr = this.currentMonth + 1
      if (day.toString().length !== 2) day = `0${day}`
      if (monthStr.toString().length !== 2) monthStr = `0${monthStr}`
      this.selectedDay = `${monthStr}/${day}/${this.currentYear}`
      console.log(this.selectedDay)

      console.log(index + ' ' + this.prevCalendarIndex)
      document.getElementById(index).classList.add('calendar-number-selected')
      if (this.prevCalendarIndex !== null) document.getElementById(this.prevCalendarIndex).classList.remove('calendar-number-selected')
      this.prevCalendarIndex = index
    },
    chooseRoom(room){
      this.roomSelected = true
      this.roomSelectedId = room.id
      console.log(this.selectedDay)
      console.log(room)
    },
    getCurrentDay(){
      let curDay = new Date()
      this.currentMonth = curDay.getMonth()
      this.currentYear = curDay.getFullYear()
      this.setCorrectMonth()
    },
    setCorrectMonth(){
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
    paintTime(index){
      console.log('paint')
      let indexStart = null
      let indexEnd = null
      if (index < this.indexSelected) {
        indexEnd = this.$data.indexSelected + 1
        indexStart = index
      }
      else {
        indexStart = this.indexSelected
        indexEnd = index + 1
      }
      let sliceArray = this.$data.timesArray.slice(indexStart, indexEnd)
      // console.log(`indexStart:${indexStart}; indexEnd:${indexEnd};`)
      for (let i of this.timesArray){
        if (this.onMousedown === true)
          if (sliceArray.includes(i))
            document.getElementById(i).classList.add('linear-table-td-painted')
          else document.getElementById(i).classList.remove('linear-table-td-painted')
      }
      this.indexStart = sliceArray[0]
      this.indexEnd = sliceArray[sliceArray.length-1]
    }
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
    //background-color: #23b24e;
  }
}
.hidden-button{
  background: inherit;
  border: none;
  display: flex;
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
.room-name{
  font-size: 14px;
  font-weight: 500;
  margin: 7px;
}
.camera:hover{
  background-color: #dadada;
  cursor: pointer;
}
.linear-table{
  background: linear-gradient(#dfe0ff 50%, #ffffff 50%);
  background-size: 100% 37px;
  &-td{
    font-size: 11px;
    &:hover{
      cursor: pointer;
    }
    &-painted {
      background-color: rgba(255, 230, 0, 0.25);
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