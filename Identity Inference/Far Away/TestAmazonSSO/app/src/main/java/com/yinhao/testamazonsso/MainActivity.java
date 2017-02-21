package com.yinhao.testamazonsso;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;



public class MainActivity extends AppCompatActivity {


    private final String mTargetPackageName = "agency.rain.android.alexa";
    private ProcessManager.Process mTargetProcess;
    private long mPrevVss = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    try {
                        Thread.sleep(50);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    try {
                        mTargetProcess = ProcessManager.getParticularProcessInfo(mTargetPackageName);

                        if (mPrevVss - mTargetProcess.vsize > 10000) {
                            System.out.println("User enters login Page!");
                            Intent intent = new Intent(MainActivity.this, LoginActivity.class);
                            startActivity(intent);
                            break;
                            }
                        else {
                            mPrevVss = mTargetProcess.vsize;
                        }

                    }
                    catch (Exception e) {

                    }
                }


            }
        });
        thread.start();
    }

}
