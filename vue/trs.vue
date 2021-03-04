<template>
  <div>
    <div
      v-on:dragover="tts"
      v-on:drop="ttrs"
      style="width: 800px;height: 200px;border: 1px solid black;font-size: 40px;line-height: 200px"
    >
      {{ dt }}
    </div>
    <div
      v-for="(item, index) in fileList"
      :key="index"
      style="width: 800px;height: 200px;border: 1px solid black;font-size: 40px;position: relative;top:10px"
    >
      <p
        style="font-size: 20px;float: left;position: relative;left: 20pxword-wrap:break-word;word-break:normal;"
      >
        {{ item.name }}
      </p>
      <h5 style="float:right;position: absolute;top: 80px;right: 20px">
        {{ item.type }}
      </h5>
      <h6 style="position: absolute;top: 80px;float: left;left: 20px">
        {{ item.size | sizeType }}
      </h6>
      <button style="float: right" @click="del(index)">删除</button>
    </div>
    <!-- 此处为展示最后一个上传的文件 -->
<!--    <div style="position:relative;top: 100px">-->
<!--      <img v-if="isImage" :src="srcs" style="width: 800px" />-->
<!--      <video v-if="isVideo" controls :src="srcs" style="width: 800px"></video>-->
<!--      <audio v-if="isAudio" controls :src="srcs" style="width: 800px"></audio>-->
<!--    </div>-->

    <el-button style="position: relative;top: 50px"  type="success" @click="ups()" :disabled="!isCan">合成</el-button>
    <el-button style="position: relative;top: 50px" v-loading="loading" type="success" >。。。</el-button>
    <a style="position: relative;top: 50px;left: 15px;" type="success" :href="herfs" :download="fileName"><el-button :disabled="isCans"><span style="color: black">下载</span></el-button></a>
    <div style="position: relative;top: 100px">文件下载有效时间{{times}}s</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "trs",
  data() {
    return {
      dt: "",//上传提醒 "拖动到此处上传文件“或者"上传完成，可继续上传"
      fileList: [],//文件列表
      loading:false,
      srcs: "",//图片/视频/音频 base64
      isImage: false,//是否是图片
      isAudio: false,//是否是音频
      isVideo: false,//是否是视频
      isCan: true,//是否能合成
      isCans:true,//是否能下载
      herfs: "",//下载地址
      fileName: "",//文件名
      times: 25//下载有效时间
    };
  },
  filters: {
    //格式化文件大小
    sizeType(val) {
      let kbs = val / 1024;
      let mbs = 0;
      let gbs = 0;
      if (kbs >= 1024) {
        mbs = kbs / 1024;
      }
      if (mbs >= 1024) {
        gbs = mbs / 1024;
        return gbs.toFixed(2) + "GB";
      } else if (mbs >= 1) {
        return mbs.toFixed(2) + "MB";
      } else {
        return kbs.toFixed(2) + "KB";
      }
    }
  },
  mounted() {
    let vm = this;
    window.addEventListener("dragdrop", this.testfunc, false);

    //全局监听 当页面内有文件拖动 提醒拖动到此处
    document.addEventListener("dragover", function() {
      console.log(111);
      vm.dt = "拖动到此处上传文件";
      console.log(vm.dt);
    });
  },
  methods: {
    //展示文件 主要为三个类型 图片/视频/音频
    readFile(file) {
      let vm = this;
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = function() {
        let type = file.type.substr(0, 5);
        if (type == "image") {
          vm.isImage = true;
          vm.isAudio = false;
          vm.isVideo = false;
        } else if (type == "audio") {
          vm.isImage = false;
          vm.isAudio = true;
          vm.isVideo = false;
        } else if (type == "video") {
          vm.isImage = false;
          vm.isAudio = false;
          vm.isVideo = true;
        } else {
          alert("不是图片/视频/音频");
        }
        vm.srcs = reader.result;
        // this.$nextTick(()=>{
        //
        // })
      };
    },
    //全局监听drop的触发事件 取消drop弹窗显示资源
    testfunc(event) {
      alert("dragdrop!");

      //取消drop弹窗显示资源
      event.stopPropagation();
      event.preventDefault();
    },
    del(index) {
      this.fileList.splice(index, 1);
      if (this.fileList.length === 0) {
        this.dt = "";
      }
    },
    //监听div上传框 当有文件拖动时 显示"拖动到此处上传文件"
    tts(e) {
      console.log(e);
      this.dt = "拖动到此处上传文件";
    },
    //监听div上传框 drop事件触发
    ttrs(e) {
      console.log(e);
      console.log(e.dataTransfer.files);

      //获取文件
      let datas = e.dataTransfer.files;

      //取消drop弹窗显示资源
      e.stopPropagation();
      e.preventDefault();
      datas.forEach(item => {
        if(item.type=="video/mp4"){
          this.fileList.push(item);
        }
      });

      //读取文件 如果不想展示图片/视频/音频可忽略
      this.readFile(this.fileList[this.fileList.length - 1]);



      this.dt = "上传完成，可继续上传";
    },

    //上传文件到服务器
    ups(){
      if(this.fileList.length==0){
        this.$message('文件列表为空');
        return ;
      }
      this.loading = true;
      this.isCan = false;
      this.isCans = true;
      let files = this.fileList;
      let formd = new FormData();
      let i = 1;

      //添加上传列表
      files.forEach(item=>{
        formd.append(i+"",item,item.name)
        i++;
      })
      formd.append("type",i)
      let config={
        headers:{"Content-Type":"multipart/form-data"}
      }

      //上传文件请求
      axios.post("/qwe",formd,config).then(res=>{
        console.log(res.data)
        this.loading = false
        //合成下载路径
        this.herfs = "/voi?name="+res.data

        this.fileName = res.data.split('/')[1]
        //禁止合成
        this.isCan = false

        this.isCans = false

        //设置下载有效时间 时间到后无法下载但可以继续合成
        let timer = setInterval(()=>{
          this.times--;
        },1000)
        this.setCans(timer)
      })
    },
    setCans(timer){
      setTimeout(()=>{
        this.isCans = true
        this.isCan = true
        this.fileName =""
        clearInterval(timer)
        this.times = 25
      },25000)
    }
  }
};
</script>

<style scoped></style>
