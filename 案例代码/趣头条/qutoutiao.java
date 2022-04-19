package com.jni;
import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.memory.Memory;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.ObjectOutputStream;

public class qutoutiao extends AbstractJni {
    private final AndroidEmulator emulator;
    private final VM vm;
    private Module module;
    String rootPath = "C:\\Users\\Desktop\\AppTest\\";
    File apkFile = new File(rootPath+"趣头条.apk");
    File soFile = new File(rootPath+"libNativeExample.so");

    // OtoB: Object to Bytes;
    private static byte[] OtoB(Object obj){
        try {
            ByteArrayOutputStream ByteStream = new ByteArrayOutputStream();
            ObjectOutputStream ObjectStream = new ObjectOutputStream(ByteStream);
            ObjectStream.writeObject(obj);
            ObjectStream.flush();
            byte[] newArray = ByteStream.toByteArray();
            ObjectStream.close();
            ByteStream.close();
            return newArray;
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }

    public qutoutiao() {
        emulator = AndroidEmulatorBuilder.for32Bit().build();
        final Memory memory = emulator.getMemory();
        memory.setLibraryResolver(new AndroidResolver(23));
        vm = emulator.createDalvikVM(apkFile);
        vm.setVerbose(false);
        vm.setJni(this);
        DalvikModule dm = vm.loadLibrary(soFile, true);
        module = dm.getModule();
        dm.callJNI_OnLoad(emulator);
        Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    emulator.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }));
    }

    public String get_sign(){
        DvmClass BitmapkitUtils = vm.resolveClass("com/jifen/qukan/utils/NativeUtils");
        String params = "OSVersion=5.1.1&deviceCode=863064707522829&device_code=863064707522829&distinct_id=d81d2cf27a955ec6&dtu=003&guid=ee4d8ab62051306258de31e88ec1.04506739&h5_zip_version=1004&innoseed=&keyword=Lx&keywordSource=search&lat=35.00024265777022&limit=20.0&lon=107.56824527000379&network=wifi&oaid=&page=1&searchSource=0&tabCode=0&time=1650004096206&tk=ACH5kAjk7kEzhC-JcKT27sgVQw5V2TuYW0Q0NzUxNDk1MDg5NTIyNQ&token=&traceId=94c370c5a88283dafd2f235f29a7762a&tuid=-ZAI5O5BM4QviXCk9u7IFQ&uuid=ba4be62de1e14e14a80f64e9e1ef42f3&version=31043000&versionName=3.10.43.000.0603.1931";
        StringObject signs = BitmapkitUtils.callStaticJniMethodObject(emulator,"innoSign()",params);
        String sign = signs.getValue();
        return sign;
    }

    public static void main(String[] args) {
        com.jni.qutoutiao qtt = new com.jni.qutoutiao();
        System.out.println(qtt.get_sign());
    }

}
