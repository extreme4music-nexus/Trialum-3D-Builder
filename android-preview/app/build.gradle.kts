plugins {
    id("com.android.application")
}
android {
    namespace = "com.trialum.gardenpreview"
    compileSdk = 36
    defaultConfig {
        applicationId = "com.trialum.gardenpreview"
        minSdk = 26
        targetSdk = 36
        versionCode = 1
        versionName = "S7-MASTER-PASS2-preview.1"
    }
    buildTypes {
        getByName("debug") { isDebuggable = true }
        getByName("release") { isMinifyEnabled = false }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    packaging { resources { excludes += setOf("META-INF/*.kotlin_module") } }
}
