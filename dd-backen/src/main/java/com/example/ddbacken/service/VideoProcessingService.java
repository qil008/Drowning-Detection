package com.example.ddbacken.service;

import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;

import java.io.*;

@Service
public class VideoProcessingService {

    private final ResourceLoader resourceLoader;

    public VideoProcessingService(ResourceLoader resourceLoader) {
        this.resourceLoader = resourceLoader;
    }
    public void processVideo_py(String fileName) throws Exception{
        // Construct the path to the Python script within the resources directory
        String pythonScriptPath = resourceLoader.getResource("classpath:process_video.py").getFile().getPath();
        ProcessBuilder processBuilder = new ProcessBuilder("python", pythonScriptPath, fileName);
        Process process = processBuilder.start();

        // get script output
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String line;
        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }

        // wait for completion
        int exitCode = process.waitFor();
        System.out.println("Python script executed with exit code " + exitCode);

        if (exitCode != 0) {
            throw new Exception("Python script execution failed with exit code " + exitCode);
        }
    }
}

