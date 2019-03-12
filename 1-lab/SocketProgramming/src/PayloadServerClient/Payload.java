package PayloadServerClient;

import java.io.Serializable;

public class Payload implements Serializable {
    private String ip;
    private String message;

    Payload(String ip, String msg) {
        this.ip = ip;
        this.message = msg;
    }

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    @Override
    public String toString() {
        return this.getIp().substring(1) + ": " + this.getMessage();
    }
}
