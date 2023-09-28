<template>
  <div class="explorer-parent">
    <div class="explorer container window">
      <div style="margin: 10px 0" class="grid-default">
        <div class="content content-start">
          <div style="width: 245px;" class="grid-default">
            <div style="font-size: 12px">
              <div>
                Название фильтр
              </div>
              <div>
                Дата фильтр
              </div>
            </div>
            <div class="content content-end">
              <input v-model.lazy="explorerFilterDay" type="date">
            </div>
          </div>
        </div>
        <div class="content content-end">
          <button style="padding: 2px 8px" class="btn btn-danger" @click="$emit('openExplorerChange')">Х</button>
        </div>
      </div>

      <div class="row">
        <div style="margin-left: 10px" class="explorer-folders col-5 window">
          <div class="camera">Папка 1</div>
          <div class="camera">Папка 2</div>
          <div class="camera">Файл 1</div>
          <div class="camera">Файл 2</div>
        </div>
        <div  style="margin-left: 15px" class="explorer-preview col-6 window">
          <div v-if="!fileSelected">Выберите файл</div>
          <div v-else>
            <div class="content content-center">
              <img
                  style="margin-top: 10px; width: 250px; height: 140px"
                  :src="require('../assets/images/img1.png')"
                  alt="предпросмотр файла">
            </div>
            <div style="margin-left: 10px">
              <div class="file-information">
                <span class="short-name" title="Название">Название: Название</span>
              </div>
              <div class="file-information">
                <span class="short-name" title="Тип">Тип: Тип</span>
              </div>
              <div class="file-information">
                <span class="short-name" title="Дата">Дата: Дата</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ExplorerPage",
  props: ['openExplorer'],
  data() {
    return{
      fileSelected: true,
      explorerFilterDay: null,
    }
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
  height: 200px;
  overflow-y: auto;
}
.explorer-preview{
  height: 300px;
  overflow-y: auto;
}
.explorer{
  width: 600px;
  height: 400px;
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
}
</style>