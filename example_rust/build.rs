use std::env;
use std::fs::File;
use std::io::Write;
use std::path::Path;
use std::process::Command;

fn rustc_version()->String {
    let cmd = Command::new(env::var("RUSTC").unwrap())
                .args(&["--version"])
                .output()
                .expect("failed to execute process");
    let mut x = String::from_utf8(cmd.stdout).unwrap();
    x = x.trim().to_string();
    if x.starts_with("rustc") {
        x = x[5..].trim().to_string();
    }
    x
}

fn pybuildinfo()->Vec<u8> {
    let pyscript = "
import os
import sys

if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.getcwd(), '..'))
    sys.path.append(path)
    import pybuildinfo.cmd
    pybuildinfo.cmd.cmd(sys.argv[2:])
";
    let dict = format!("-dict={}", format!("{{
        \"build_toolchain\": \"rustc\",
        \"build_toolchain_version\": \"{}\",
        \"build_target\": \"{}\"
    }}", rustc_version(), env::var("TARGET").unwrap()));

    let cmd = Command::new("python")
                .args(&["-c", pyscript, "-vcs=\"..\"", "-template=buildinfo_template.rs", &dict])
                .output()
                .expect("failed to execute process");
    assert_eq!(cmd.status.code().unwrap(), 0);
    cmd.stdout
}

fn main() {
    let out_dir = env::var("OUT_DIR").unwrap();
    let dest_path = Path::new(&out_dir).join("pybuildinfo.rs");
    let mut f = File::create(&dest_path).unwrap();
    let buildinfo = pybuildinfo();
    f.write_all(&buildinfo).unwrap();
}
