package ces.bachelor.coffeetime;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Typeface;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

public class Login extends AppCompatActivity {

    SharedPreferences token;
    Intent mainClass;

    public void scan(View view){
        new IntentIntegrator(this).initiateScan();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        mainClass = new Intent(this, MainActivity.class);

        if(getIntent().getStringExtra("update") == null){
            token = this.getSharedPreferences("ces.bachelor.coffetime", Context.MODE_PRIVATE);
            String tempToken = token.getString("token", "");

            if (!tempToken.equals("")) {
                startActivity(mainClass);
                finish();
            }
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        IntentResult result = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);
        if(result != null) {
            if(result.getContents() == null) {
                Log.d("MainActivity", "Cancelled scan");
                Toast.makeText(this, "Cancelled", Toast.LENGTH_LONG).show();
            } else {
                Log.d("MainActivity", "Scanned");
                token.edit().putString("token", result.getContents()).apply();
                startActivity(mainClass);
                finish();
            }
        } else {
            // This is important, otherwise the result will not be passed to the fragment
            super.onActivityResult(requestCode, resultCode, data);
        }
    }
}
