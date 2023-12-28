<template>
    <div>
        Choose File: <input type="file" ref="fileInputRef" @change="selectFile">
        <br />
        <button type="primary" @click="uploadFile">Upload</button>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Upload',
    methods: {
        selectFile() {
            let file = this.$refs['fileInputRef'].files[0]
            if (file) {
                console.log(`Selected file: ${file.name}`);
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
                }
            }).catch(error => {
                alert(`Upload error: ${error.message}`);
            });

            this.$refs['fileInputRef'].value = ''
        }
    }
}
</script>

<style></style>
