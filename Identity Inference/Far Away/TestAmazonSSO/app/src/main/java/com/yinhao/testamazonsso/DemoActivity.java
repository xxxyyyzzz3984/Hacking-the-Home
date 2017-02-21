package com.yinhao.testamazonsso;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class DemoActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_demo);

        String name = getIntent().getStringExtra("USER_NAME");
        String email = getIntent().getStringExtra("USER_EMAIL");
        String account = getIntent().getStringExtra("USER_ACCOUNT");
        String zipcode = getIntent().getStringExtra("USER_ZIPCODE");

        TextView name_text = (TextView) findViewById(R.id.nametext);
        name_text.setText(name);

        TextView email_text = (TextView) findViewById(R.id.emailtext);
        email_text.setText(email);

        TextView account_text = (TextView) findViewById(R.id.accounttext);
        account_text.setText(account);

        TextView zipcode_text = (TextView) findViewById(R.id.zipcodetext);
        zipcode_text.setText(zipcode);
    }
}
