<template>
  <div class="explorer-parent">
    <div class="explorer container window">
      <div class="grid-default">
        <div style="margin-top: 5px" class="content content-start">
          <input @keydown.enter="getByRoutesCall(null); resetFile()"
                 v-model.trim="routeToFile"
                 class="input-field input-field-file"
                 type="text"
                 placeholder="Путь до папки с архивными файлами">
          <button @click="getByRoutesCall(null); resetFile()" class="btn btn-success">Открыть</button>
        </div>
        <div class="content content-end">
          <button style="padding: 2px 8px" class="btn btn-danger" @click="$emit('closeExplorer')">Х</button>
        </div>
      </div>
      <div style="margin: 10px 0" class="grid-default">
        <div class="content content-start">
          <div style="width: 245px;" class="grid-default grid-default-folderParams">
            <div style="font-size: 12px">
              <div class="grid-default" style="width: 60px">
                <div class="content content-start">
                  <button @click="changePage('prev')" class="hidden-button">
                    <img :src="require('../assets/icons/arrow-left.png')">
                  </button>
                </div>
                <div class="content content-end">
                  <button @click="changePage('next')" class="hidden-button">
                    <img :src="require('../assets/icons/arrow-right.png')">
                  </button>
                </div>
              </div>
              <div>
                <button style="font-size: 15px; margin-right: 5px" class="camera hidden-button"
                        @click="sortByValue('name'); filterType = 'name'">
                  Имя
                </button>
                <img :style="filterType === 'createTime' ? {display: 'none'} : {}"
                     id="btn-img-name"
                     :src=" require(`../assets/icons/${imgPath}`)">
              </div>
              <div>
                <button style="font-size: 15px; margin-right: 5px" class="camera hidden-button"
                        @click="sortByValue('createTime'); filterType = 'createTime'">
                  Дата
                </button>
                <img :style="filterType === 'name' ? {display: 'none'} : {}"
                     id="btn-img-createTime"
                     :src="require(`../assets/icons/${imgPath}`)">
              </div>
            </div>
            <div style="display: flex; align-items: center">
              <div >
                <div>
                  <input
                      class="input-field input-field-fileName"
                      v-model.trim="explorerFilterName"
                      @input="sortByDayName"
                      type="text"
                      placeholder="Поиск по названию">
                </div>
                <div>
                  <input
                      class="input-field input-field-fileName"
                      v-model.trim="explorerFilterDay"
                      @change="sortByDayName"
                      type="date">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div style="margin-left: 10px" class="explorer-folders col-5 window">
          <div @dblclick="getByRoutesCall(file)"
               class="camera"
               v-for="(file, index) in this.getFiles"
               :key="index"
               onmousedown="return false">
            <img
                :src="file.type === 'file' ? require('../assets/icons/file.png') : require('../assets/icons/folder.png')"
                alt=""
                style="margin-bottom: 10px; margin-right: 5px">
            <span class="short-name short-name-file" :title="file.name">{{file.name}}</span>
            <span class="short-name short-name-file fileDate"
                  v-if="file.createTime"
                  :title="corrDate(file.createTime)">
              {{corrDate(file.createTime)}}
            </span>
          </div>
        </div>
        <div  style="margin-left: 15px" class="explorer-preview col-6 window">
          <div v-if="!fileSelected">Выберите файл</div>
          <div v-else>
            <div class="content content-center">
              <img
                  style="margin-top: 10px; width: 250px; height: 140px"
                  :src="file.imageSrc"
                  alt="предпросмотр файла">
            </div>
            <div style="margin-left: 10px">
              <div class="file-information">
                <span class="short-name" :title="file.name">Название: {{file.name}}</span>
              </div>
<!--              <div class="file-information">-->
<!--                <span class="short-name" :title="file.type">Тип: {{file.type}}</span>-->
<!--              </div>-->
              <div class="file-information">
                <span class="short-name" :title="file.createTime">Дата: {{file.createTime}}</span>
              </div>
              <button @click="$emit('openCalendar'); $store.state.file = file" class="btn btn-success">Подтвердить</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: "ExplorerPage",
  props: ['openExplorer', 'selectFunction'],
  data() {
    return{
      filterType: 'name',
      imgPath: 'arrow-up.png',

      file: {
        name: '',
        createTime: '',
        type: '',
        imageSrc: 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='
      },
      fileRoute: '',
      fileSelected: false,
      explorerFilterDay: '',
      explorerFilterName: '',
      routeToFile: null,

      filterDefault: true,
      foldersInfo: {
        folders: [],
        page: 0,
      }
    }
  },
  mounted() {
    this.$store.state.files = []
  },
  computed: {
    ...mapGetters([
      'getFiles',
      'getFile',
      'getFilesByDay',
      'getFilesByName'
    ])
  },
  methods: {
    async getByRoutesCall(file){
      let data = {baseRoute: this.routeToFile}
      if (file !== null){
        if (file.type === 'dir'){
          this.fileRoute += `${file.name}\\`
          data.curRoute = this.fileRoute
        }
        else if (this.fileRoute !== ''){
          data.curRoute = this.fileRoute
        }
        if (file.type === 'file') data.fileName = file.name
      }
      this.foldersInfo.folders = []
      this.fileRoute.split('\\').forEach((value) => {
        this.foldersInfo.folders.push(value)
      })
      this.foldersInfo.page = this.foldersInfo.folders.length -1
      let resp = await this.selectFunction(this.getByRoutes, data)
      try {
        if (resp.image){
          this.fileSelected = true
          this.file = resp
          this.file.createTime = `${this.corrDate(resp.createTime)}`
          this.file.imageSrc = `data:image/jpg;base64,${resp.image}`
        }
        else if (resp.folderData){
          this.sortByValue('default')
          this.filterType = 'name'
        }
      } catch (err) {
        console.log(err)
      }
    },
    corrDate(incorrDate){
      try{
        let value = new Date(incorrDate.substring(0, incorrDate.length-4))
        let year = value.getFullYear()
        let date = value.getDate().toString().length === 1 ? `0${value.getDate()}` : value.getDate()
        let month = value.getMonth().toString().length === 1 ? `0${value.getMonth()+1}` : value.getMonth()+1
        let hour = value.getHours().toString().length === 1 ? `0${value.getHours()}` : value.getHours()
        let minute = value.getMinutes().toString().length === 1 ? `0${value.getMinutes()}` : value.getMinutes()
        let second = value.getSeconds().toString().length === 1 ? `0${value.getSeconds()}` : value.getSeconds()
        return `${date}.${month}.${year} ${hour}:${minute}:${second}`
      } catch (err) {
        console.log(err)
      }
    },
    sortByValue(sortValue) {
      if (sortValue === 'default'){ // сортировка по имени без изменения порядка
        sortValue = 'name'
        this.filterType = 'name'
      }
      else this.filterDefault = !this.filterDefault// сортировка по значению с изменением порядка

      if (this.filterDefault){
        this.getFiles.sort((a, b) => sortValue === 'name'
            ? (a[sortValue].toLowerCase() < b[sortValue].toLowerCase() ? 1 : -1)
            : (a[sortValue] < b[sortValue] ? 1 : -1))
        this.imgPath = 'arrow-up.png'
      }
      else{
        this.imgPath = 'arrow-down.png'
        this.getFiles.sort((a, b) => sortValue === 'name'
            ? (a[sortValue].toLowerCase() > b[sortValue].toLowerCase() ? 1 : -1)
            : (a[sortValue] > b[sortValue] ? 1 : -1))
      }
      this.getFiles.sort((a, b) => a['type'] > b['type'] ? 1 : -1)
    },
    sortByDayName(){
      this.getByRoutesCall(null).then(() => {
        console.log('1')
        if (this.explorerFilterDay !== '') this.$store.state.files = this.getFilesByDay(new Date(this.explorerFilterDay))
        console.log('2')
        if (this.explorerFilterName !== '') this.$store.state.files = this.getFilesByName(this.explorerFilterName)
        // for (let file in this.getFiles)
        // else this.getByRoutesCall(null)
      })
    },
    // sortByName(){
    //   this.getByRoutesCall(null).then(() => {
    //     if (this.explorerFilterName !== '') this.$store.state.files = this.getFilesByName(this.explorerFilterName)
    //   })
    // },
    prevNextFolder() {
      let path = ''
      for (let i = 0; i < this.foldersInfo.page; i++){
        console.log(this.foldersInfo.folders[i])
        path += `${this.foldersInfo.folders[i]}\\`
      }
      this.fileRoute = path
      let data = {
        baseRoute: this.routeToFile,
        curRoute: this.fileRoute}
      this.selectFunction(this.getByRoutes, data).then(() => {
        this.sortByValue('default')
      })
    },
    changePage(value){
      if (value === 'prev' && this.foldersInfo.page !== 0) {
        this.foldersInfo.page -= 1
        this.prevNextFolder()
      }
      else if (value === 'next' && this.foldersInfo.page !== this.foldersInfo.folders.length) {
        this.foldersInfo.page += 1
        this.prevNextFolder()
      }
    },
    resetFile(){
      this.explorerFilterName = ''
      this.explorerFilterDay = ''
      this.file.name = ''
      this.file.createTime = ''
      this.file.type = ''
      this.file.imageSrc = 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='
      this.fileRoute = ''
      this.foldersInfo = {
        folders: [],
        page: 0
      }
    },
    ...mapActions([
        'getByRoutes'
    ])
    }
}
</script>

<style scoped lang="scss">
.explorer-parent {
  width: 100%;
  height: 100%;
  position: fixed;
  left: 0;
  top: 0;
  display: flex;
  align-items: center;
//align-content: center;
  justify-content: center;
  z-index: 100;
  background-color: rgba(218, 218, 218, 0.7);
}
.explorer-folders{
  height: 300px;
  overflow-y: auto;
}
.explorer-preview{
  height: 300px;
  overflow-y: auto;
}
.explorer{
  width: 600px;
  height: 500px;
  background-color: #ffffff;
}
.camera:hover{
  background-color: #dadada;
  cursor: pointer;
}
.window{
  box-shadow: 0 3px 4px rgba(0,0,0,.25);
  border-radius: 10px ;
}
.grid-default{
  display: grid;
  grid-gap: 10px;
  grid-template-columns: 1fr 1fr;
  &-folderParams{
    grid-template-columns: 2fr 1fr;
  }
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
  &-fileName {
    margin: 5px;
    width: auto;
    position: relative;
  }
}
//.file-information{
//  width: 100%;
//}
.short-name {
  display: inline-block;
  width: 250px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  &-file {
    width: 80%;
    font-size: 14px;
  }
}
.fileDate{
  font-size: 12px
}
.hidden-button{
  background: inherit;
  border: none;
  align-items: center;
  justify-content: center;
}

</style>