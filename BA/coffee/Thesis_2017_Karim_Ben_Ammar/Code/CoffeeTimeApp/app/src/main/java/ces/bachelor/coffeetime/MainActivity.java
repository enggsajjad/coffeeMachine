package ces.bachelor.coffeetime;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.CheckBox;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;


import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.w3c.dom.Text;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    private CheckBox milk;
    private RadioGroup radioGroup;
    private String choice;
    private boolean ready;
    private String token;
    private String coffee;
    private String water;
    private String withMilk;

    private TextView user;
    private TextView balance;
    private TextView lastChoice;

    private static final String BASE_URL = "http://141.3.72.128:8888/";
    public static final String KEY_TOKEN = "token";
    public static final String KEY_WATER = "water";
    public static final String KEY_COFFEE = "coffee";
    public static final String KEY_MILK = "milk";

    public void onStart(View view){

        if(ready){
            switch(choice) {
                case "water": {
                    coffee = "false";
                    water = "true";
                    break;
                }
                case "coffee" : {
                    water = "false";
                    coffee = "true";
                    break;
                }
            }
            withMilk = String.valueOf(milk.isChecked());
            order();
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ready = false;
        Toolbar myToolbar = (Toolbar) findViewById(R.id.my_toolbar);
        myToolbar.setTitle("");
        setSupportActionBar(myToolbar);
        SharedPreferences tempToken = this.getSharedPreferences("ces.bachelor.coffetime", Context.MODE_PRIVATE);

        user = (TextView) findViewById(R.id.user);
        balance = (TextView) findViewById(R.id.balance);
        lastChoice = (TextView) findViewById(R.id.lastChoice);

        token = tempToken.getString("token", "");
        coffee = "";
        water = "";
        withMilk = "";
       // milk = (CheckBox)findViewById(R.id.checkMilk);

        /*radioGroup = (RadioGroup)findViewById(R.id.radioGroup);

        radioGroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                ready = true;
                if(checkedId == R.id.water) {
                    milk.setEnabled(false);
                    milk.setChecked(false);
                    choice = "water";
                } else if (checkedId == R.id.coffee){
                    milk.setEnabled(true);
                    choice = "coffee";
                }
            }
        });*/

        this.updateUser();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.option_menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if(item.getItemId() == R.id.newToken){
            startActivity(new Intent(this, Login.class).putExtra("update", "yes"));
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private void order(){
        StringRequest stringRequest = new StringRequest(Request.Method.POST, BASE_URL,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        Toast.makeText(MainActivity.this,response,Toast.LENGTH_LONG).show();
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(MainActivity.this,error.toString(),Toast.LENGTH_LONG).show();
                    }
                }
        ){
            @Override
            protected Map<String, String> getParams(){
                Map<String,String> params = new HashMap<String, String>();
                params.put(KEY_TOKEN, token);
                params.put(KEY_WATER, water);
                params.put(KEY_COFFEE, coffee);
                params.put(KEY_MILK, withMilk);
                return params;
            }1
        };
        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(stringRequest);
    }

    private void updateUser(){
        RequestQueue queue = Volley.newRequestQueue(this);
        String url ="http://i80misc01.itec.kit.edu/coffee/getuser.php?rfid=" + token;

        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                            String delim = "[;]";
                            String[] temp = response.split(delim);
                            balance.setText("Balance : " + Float.toString(Float.parseFloat(temp[2]) / 100) + " €");
                            user.setText("Welcome " + temp[1]);
                            if(temp[4].contains("yes")){
                                lastChoice.setText("Last choice : with milk");
                            } else {
                                lastChoice.setText("Last choice : without milk");
                            }
                        }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                user.setText("Unkown user");
            }
        });
        queue.add(stringRequest);
    }
}