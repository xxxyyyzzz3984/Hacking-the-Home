package com.yinhao.stealingwifiscan;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.SwitchCompat;
import android.view.View;
import android.widget.CompoundButton;
import android.widget.TextView;
import android.widget.Toast;

import com.spark.submitbutton.SubmitButton;

import java.io.IOException;

public class MainActivity extends AppCompatActivity implements ThreadCompleteListener {

    private TextView mSwitchText;
    private SwitchCompat mAttackSwitch;
    private HomeDeviceInfo mGHDInfo;
    private ProgressDialog mLoadingDlg;
    private SubmitButton mViewLocationBtn;
    public static String OurHomeMac = "F4:F5:D8:C1:B9:2E";
    private String mGHDIP = "";
    public static String mScanResults;
    private NotifyingThread mAttackThread;
    private String AttackThreadLabel = "attack_thread";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mSwitchText = (TextView) findViewById(R.id.switchText);
        mAttackSwitch = (SwitchCompat) findViewById(R.id.AttackSwitch);

        mAttackSwitch.setChecked(false);
        mLoadingDlg = new ProgressDialog(MainActivity.this);
        mLoadingDlg.setMessage("Searching for Target Google Home and Exploit, Please Hold......");
        mLoadingDlg.setCancelable(false);
        mLoadingDlg.setInverseBackgroundForced(false);

        mViewLocationBtn = (SubmitButton) findViewById(R.id.viewlcbtn);
        mViewLocationBtn.setVisibility(View.INVISIBLE);
        mViewLocationBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showLocation(v);
            }
        });

        //response to attack switch
        mAttackSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(isChecked){

                    mSwitchText.setText("Attack is on");
                    mSwitchText.setTextColor(getResources().getColor(R.color.colorAccent));
                    initilize_attackthread();
                    mAttackThread.start();
                    mLoadingDlg.show();

                }else{
                    mSwitchText.setText("Attack is off");
                    mSwitchText.setTextColor(getResources().getColor(R.color.colorGrey));
                    mAttackThread.interrupt();
                }

            }
        });
    }

    private void initilize_attackthread() {
        mAttackThread = new NotifyingThread() {
            @Override
            public void doRun() {
//                try {
//                    mGHDInfo = new HomeDeviceInfo();
//                    mGHDIP = mGHDInfo.getIPfromMac(OurHomeMac);
//                    if (!mGHDIP.matches("")) {
//                        System.out.println("Google Home Device Found!! With IP Address " + mGHDIP);
//                        mScanResults = mGHDInfo.getScanResults();
//                    }
//                }
//                catch (IOException e) {
//                    e.printStackTrace();
//                }
            }
        };

        mAttackThread.label = AttackThreadLabel;
        mAttackThread.addListener(MainActivity.this);

    }

    public void showLocation(View v)
    {
        AsyncTask.execute(new Runnable() {
            @Override
            public void run() {
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                Intent showloc_intent = new Intent(MainActivity.this, ShowLocationActivity.class);
                startActivity(showloc_intent);
            }
        });

    }



    @Override
    public void notifyOfThreadComplete(NotifyingThread thread) {
        //wait for Attack Thread to finish
        if (thread.label.matches(AttackThreadLabel)) {


            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    mSwitchText.setText("Attack is off");
                    mSwitchText.setTextColor(getResources().getColor(R.color.colorGrey));
                    mAttackSwitch.setChecked(false);
                }
            });

            //send packets to server
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    mLoadingDlg.hide();
                    Toast.makeText(MainActivity.this, "Data has been collected", Toast.LENGTH_LONG).show();
                    mViewLocationBtn.setVisibility(View.VISIBLE);
                }
            });
        }

    }
}
