package com.yinhao.stealingwifiscan;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

/**
 * Created by xyh3984 on 2/13/17.
 */
public class IOStreamProcessing {

    public static String readStream(InputStream is) {
        try {
            ByteArrayOutputStream bo = new ByteArrayOutputStream();
            int i = is.read();
            while(i != -1) {
                bo.write(i);
                i = is.read();
            }
            return bo.toString();
        } catch (IOException e) {
            return "";
        }
    }

    public static void writeStream(OutputStream out){
        String output = "Hello world";
        try {
            out.write(output.getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }
        try {
            out.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
