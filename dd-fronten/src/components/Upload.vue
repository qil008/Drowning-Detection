<template>
    <div>
        Choose File: <input type="file" ref="fileInputRef" @change="selectFile">
        <br />
        <button type="primary" @click="uploadFile">Upload</button>
        <!-- Video player and download button will only show after a response of successful upload  -->
        <!-- <video v-if="processedVideoUrl" controls width="320">
            <source :src="processedVideoUrl" type="video/mp4">
            Your browser does not support the video tag.
        </video> -->
        <button v-if="processedVideoUrl" @click="downloadVideo">Download Video</button>
    </div>
</template>
  
<script>
import axios from 'axios';

export default {
    name: 'Upload',
    data() {
        return {
            processedVideoUrl: '', // URL for the processed video
            newVideoName: '', // The new name of the uploaded video (same as processed video)
        }
    },
    methods: {
        selectFile() {
            let file = this.$refs['fileInputRef'].files[0]
            if (file) {
                console.log(`Selected file: ${file.name}`);
                this.processedVideoUrl = ''; // hide download button when new video is selected and before upload completion.
            } else {
                console.log("No file selected");
            }
        },
        uploadFile() {
            let file = this.$refs['fileInputRef'].files[0]

            if (!file) {
                alert("Please select a file to upload.");
                return;
            }

            let formData = new FormData()
            formData.append('file', file)

            axios({
                url: 'http://localhost:8080/video/upload',
                method: 'post',
                data: formData,
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(res => {
                console.log('Response:', res);
                if (res.data.resCode !== '200') {
                    alert(`Error: ${res.data.resCode}, Message: ${res.data.message}`);
                } else {
                    alert('File uploaded successfully.');
                    // Save the new video name and construct the URL for the processed video
                    this.newVideoName = res.data.newVideoName;
                    this.processedVideoUrl = `http://localhost:8080/video/download/${this.newVideoName}`;
                }
            }).catch(error => {
                alert(`Upload error: ${error.message}`);
            });

            this.$refs['fileInputRef'].value = ''
        },
        downloadVideo() {
            // Use the HTML5 download attribute to download the video
            const link = document.createElement('a');
            link.href = this.processedVideoUrl;
            link.download = this.newVideoName;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}
</script>
  
<style></style>
  