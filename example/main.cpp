#include <iostream>
#include <iomanip>
#include <sstream>
#include <buildinfoexample.hpp>

template<typename A, typename B>
static void print(A name, B value){
    size_t width = 14;
    ::std::cout << "\t";
    ::std::cout << ::std::left << ::std::setw(width) << ::std::setfill(' ') << name;
    bool offset = false;
    ::std::stringstream ss;
    ss << value;
    auto val = ss.str();
    for(char x : val){
        if(offset){
            ::std::cout << ::std::endl << "\t";
            ::std::cout << ::std::left << ::std::setw(width) << ::std::setfill(' ') << "";
            offset = false;
        }
        if(x == '\n'){
            offset = true;
        }
        else if(x != '\r'){
            ::std::cout << x;
        }
    }
    if(offset || val.empty() || val.back() != '\n')
        ::std::cout << std::endl;
}

int main(){
    std::cout << "scm:\t" << BuildInfo::scm_name << std::endl;

    print("hash", BuildInfo::scm_revisions_short + " / " + BuildInfo::scm_revisions);
    print("time", BuildInfo::scm_rfc2822);
    print("timestamp", BuildInfo::scm_timestamp);
    print("branch", BuildInfo::scm_branch);
    if(!BuildInfo::scm_author_email.empty())
        print("author", BuildInfo::scm_author + " <" + BuildInfo::scm_author_email + ">");
    else
        print("author", BuildInfo::scm_author);
    if(BuildInfo::scm_message_escaping.find('\n') == ::std::string::npos){
        print("message", BuildInfo::scm_message_escaping);
    }
    else{
        print("message:", "-----------------------");
        print("", BuildInfo::scm_message_escaping);
        print("", "-----------------------");
    }
    print("tags", BuildInfo::scm_version_tags);
    print("version", BuildInfo::scm_version + (BuildInfo::scm_version_stable ? "  stable" : "  unstable"));
    print("major", BuildInfo::scm_version_major);
    print("minor", BuildInfo::scm_version_minor);
    print("patch", BuildInfo::scm_version_patch);
    std::cout << std::endl;

    std::cout << "build:" << std::endl;
    print("time", BuildInfo::build_rfc2822);
    print("timestamp", BuildInfo::build_timestamp);
    print("sys", BuildInfo::build_system);
    print("sys_ver", BuildInfo::build_system_version);
    print("sys_arch", BuildInfo::build_machine);
    print("node", BuildInfo::build_node_login + "@" + BuildInfo::build_node);
    print("toolchain", BuildInfo::build_toolchain);
    print("toolchain_ver", BuildInfo::build_toolchain_version);
    print("target_sys", BuildInfo::build_target_system);
    print("targer_arch", BuildInfo::build_target_machine);
}
