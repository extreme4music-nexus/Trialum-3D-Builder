plugins {
    id("com.android.application")
}
android {
    namespace = "com.trialum.gardenpreview"
    compileSdk = 36
    defaultConfig {
        applicationId = "com.trialum.gardenpreview.g02stone"
        minSdk = 26
        targetSdk = 36
        versionCode = 2
        versionName = "S7-G02-STONE-preview.2"
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
