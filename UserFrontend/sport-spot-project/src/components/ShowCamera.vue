<template>
  <div class="col-12 window">
    <p>Изображение</p>
    <div style="width: 400px; height: 300px">
      <img
          v-if="cameraSelected"
          :src="cameraSelected ? imgPath : '' "
          style="width: 100%; height: 100%"
          alt="">
      <img v-if="!cameraSelected" :src="require('@/assets/images/background.png')" alt="">
      <canvas
          @click="drawLine($event.clientX, $event.clientY)"
          id="canvas"
          width="400" height="300"
          style="position: absolute; top: 0; left: 0; margin-top: 40px; margin-left: 14px">
      </canvas>
    </div>
    <br>
    <button @click="endDraw(); selectFunction(setSectorToDB, sector)">Заполнить область</button>
    <button @click="removeSectorPoints(); selectFunction(setSectorToDB, sector)">Очистить всё</button>
    <br>
    <span>Информация сектора</span>
    <br>
    <span class="short-name" :title="sector.name">Сектор {{sector.name}}</span>
    <br>
    <span>Техническая информация:</span>
    <ul>
      <li>
      <span class="short-name" :title="sector.points">Границы:</span>
      </li>
      <li>Высота от пола:</li>
      <li>Тип сектора: <span v-if="sectorSelected">{{getSectorTypeByID(sector.typeId).name}}</span></li>
    </ul>
    <p>Справка:</p>
  </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  props: ['cameraID', 'sector', 'selectFunction', 'sectorSelected', 'cameraSelected', 'save'],
  name: "ShowCamera",
  data(){
    return{
      imgPath: '',
      ctx: null,
      canvas: null
    }
  },
  computed: {
    ...mapGetters([
        'getSectorTypeByID',
        'getRefreshInterval'
    ])
  },
  mounted() {
    this.draw()
  },
  methods: {
    async drawImage() {
      let changeResp = await this.changeImgPath(`http://localhost:5000/getVideo?camId=${this.cameraID}`)
      console.log(changeResp)
      let interval = this.getRefreshInterval
      if (interval){
        console.log('clean')
        this.$store.commit('clearRefreshInterval')
      }
      interval = setInterval(() => this.selectFunction(this.refreshVideo), 5000)
      this.$store.commit('setRefreshInterval', interval)
    },
    async refreshVideo() {
      let returnResult
      try{
        returnResult = await fetch(`http://localhost:5000/refreshVideo?camId=${this.cameraID}`, {
          credentials: "include",
          method: 'GET',
          cors: 'no-cors',
          headers: {
            'Content-Type': 'application/json;charset=utf-8',
          },
        })
            .then(response => response.json())
            .then((response) => {
              console.log('refreshId ')
              console.log(response)
              return response
            });
      } catch (err) {
        console.log(err)
      }
      return returnResult
    },
    async changeImgPath(path){
      this.imgPath = path
      return 'ok'
    },
    draw() {
      let canvas = document.getElementById('canvas')
      if (canvas.getContext) {
        console.log('getContext')
        this.ctx = canvas.getContext("2d")
        this.canvas = canvas
        this.ctx.beginPath()
      }
    },
    drawLine(x, y){
      if (this.sectorSelected){
        let targetCoords = document.getElementById('canvas').getBoundingClientRect()
        let newX = x - targetCoords.left
        let newY = y - targetCoords.top
        console.log(`x: ${x} y: ${y} newX: ${newX} newY: ${newY} left: ${targetCoords.left} right: ${targetCoords.top}`)
        if (this.drawClicks === 0) {
          this.ctx.moveTo(newX, newY)
        }
        else this.ctx.lineTo(newX, newY)
        this.$emit('pushSectorPoints', [newX, newY])
        this.ctx.arc(newX, newY, 2, 0, Math.PI * 2)
        this.ctx.strokeStyle = "rgba(255, 230, 0)"
        this.ctx.lineWidth = 2
        this.ctx.stroke()
        this.drawClicks ++
      }
      else alert("Выберите сектор")
    },
    endDraw() {
      if (this.sector.points.length === 0) return ''
      this.ctx.lineTo(this.sector.points[0][0], this.sector.points[0][1])
      this.ctx.stroke()
      this.ctx.fillStyle = "rgba(255, 230, 0, 0.25)"
      this.ctx.fill()
      this.drawClicks = 0
    },
    drawSectorPoints() {
      let interval = setInterval(() => {
        console.log('check')
        if (this.sector.id !== null){
          clearInterval(interval)
          console.log('drawSectorPoints')
          let points = this.sector.points
          console.log(this.sector)
          this.ctx.moveTo(points[0][0], points[0][1])
          this.ctx.arc(points[0][0], points[0][1], 2, 0, Math.PI * 2)
          for (let i = 1; i < points.length; i++){
            this.ctx.lineTo(points[i][0], points[i][1])
            this.ctx.arc(points[i][0], points[i][1], 2, 0, Math.PI * 2)
          }
          this.ctx.lineTo(points[0][0], points[0][1])
          this.ctx.strokeStyle = "rgba(255, 230, 0)"
          this.ctx.fillStyle = "rgba(255, 230, 0, 0.25)"
          this.ctx.lineWidth = 2
          this.ctx.stroke()
          this.ctx.fill()
        }
      }, 10)

    },
    removeSectorPoints(){
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height)
      this.$emit('removeSectorPoints')
      this.ctx.beginPath()
    },
    drawClear() {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height)
      this.ctx.beginPath()
    },
    ...mapActions([
        'setSectorToDB'
    ])
  }
}
</script>

<style scoped>
canvas {
  border: 1px solid black;
  background: none;
}
.short-name {
  display: inline-block;
  width: 15em;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>