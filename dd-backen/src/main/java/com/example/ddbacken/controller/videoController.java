package com.example.ddbacken.controller;
import com.example.ddbacken.service.VideoProcessingService;
import org.springframework.beans.factory.annotation.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import jakarta.servlet.http.HttpServletResponse;


import java.util.*;
import java.io.*;

@RestController
@RequestMapping("/video")
public class videoController {

    @Value("${video.save-path}")
    private String savePath;

    @Value("${video.result-path}")
    private String resultPath;

    @Value("${video.max-size}")
    private long maxFileSize;

    @Autowired
    private VideoProcessingService videoProcessingService;

    @CrossOrigin(origins = "*", maxAge = 10800)
    @PostMapping(value = "/upload")
    @ResponseBody
    public Map<String, String> upload(@RequestParam("file") MultipartFile file) throws IllegalStateException {

        Map<String, String> resultMap = new HashMap<>();

        try {
            if (!file.isEmpty() && file.getSize() <= maxFileSize) {
                String fileExt = file.getOriginalFilename().substring(file.getOriginalFilename().lastIndexOf(".") + 1).toLowerCase();

                // 检查文件后缀是否为视频类型
                if (fileExt.matches("mp4|avi|flv|wmv|mov")) {
                    String newVideoName = UUID.randomUUID().toString().replaceAll("-", "") + "." + fileExt;

                    File fileSave = new File(savePath, newVideoName);
                    if (!fileSave.getParentFile().exists()) {
                        fileSave.getParentFile().mkdirs();
                    }

                    file.transferTo(fileSave);

                    try {
                        // Process the video using the service
                        videoProcessingService.processVideo_py(newVideoName);
                        resultMap.put("resCode", "200");
                        resultMap.put("newVideoName", newVideoName);
                        // Update resultMap if needed
                    } catch (Exception e) {
                        e.printStackTrace();
                        resultMap.put("resCode", "500");
                        resultMap.put("message", "Error processing video.");
                    }

                } else {
                    resultMap.put("resCode", "400");
                    resultMap.put("message", "Unsupported file type.");
                }
            } else {
                resultMap.put("resCode", "400");
                resultMap.put("message", "File is empty or exceeds maximum size limit.");
            }

            return resultMap;
        } catch (Exception e) {
            e.printStackTrace();
            resultMap.put("resCode", "500");
            resultMap.put("message", "Internal server error.");
            return resultMap;
        }
    }

    @CrossOrigin(origins = "*", maxAge = 10800)
    @GetMapping("/download/{path}")
    public Map<String, String> download (@PathVariable("path") String path, HttpServletResponse response) {
        Map<String, String> resultMap = new HashMap<>();
        File file = new File(resultPath + "/" + path);
        byte[] bytes = new byte[1024];
        if (file.exists()) {
            try (OutputStream os = response.getOutputStream();
                 FileInputStream fis = new FileInputStream(file)) {
                while ((fis.read(bytes)) != -1) {
                    os.write(bytes);
                    os.flush();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            resultMap.put("resCode", "200");
            resultMap.put("message", "Completed.");
        } else{
            resultMap.put("resCode", "400");
            resultMap.put("message", "File does not exist.");
        }
        return resultMap;
    }
}
