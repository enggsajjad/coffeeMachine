package ces.bachelor.coffeetime;

import android.content.Context;
import android.content.SharedPreferences;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.widget.EditText;

public class Settings extends AppCompatActivity {

    private EditText limitPerMonth;
    private EditText limitPerDay;
    private SharedPreferences settings;

    public void save(){

    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        Toolbar myChildToolbar = (Toolbar) findViewById(R.id.child_toolbar);
        setSupportActionBar(myChildToolbar);
        ActionBar ab = getSupportActionBar();
        ab.setDisplayHomeAsUpEnabled(true);

        limitPerMonth = (EditText) findViewById(R.id.coffeesPerMonth);
        limitPerDay = (EditText) findViewById(R.id.coffeesPerDay);

        settings = this.getSharedPreferences("ces.bachelor.coffetime", Context.MODE_PRIVATE);
        String tempToken = settings.getString("limitPerMonth", "");

        limitPerMonth.setText("0");
        limitPerDay.setText("0");
    }
}
