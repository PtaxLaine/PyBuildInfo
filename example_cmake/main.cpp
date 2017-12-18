#include <iostream>
#include <iomanip>
#include <sstream>
#include <pybuildinfoexample.hpp>

int main(){
    using namespace std;
    using namespace pybuildinfo;

    int width = 32;

    cout << left;
    cout << setw(width) << "vcs::name" << vcs::name << endl;
    cout << setw(width) << "vcs::revision" << vcs::revision << endl;
    cout << setw(width) << "vcs::revision_short" << vcs::revision_short << endl;
    cout << setw(width) << "vcs::revision_version" << vcs::revision_version << endl;
    cout << setw(width) << "vcs::revision_version_tag" << vcs::revision_version_tag << endl;
    cout << setw(width) << "vcs::revision_version_major" << vcs::revision_version_major << endl;
    cout << setw(width) << "vcs::revision_version_minor" << vcs::revision_version_minor << endl;
    cout << setw(width) << "vcs::revision_version_patch" << vcs::revision_version_patch << endl;
    cout << setw(width) << "vcs::revision_version_stable" << vcs::revision_version_stable << endl;
    cout << setw(width) << "vcs::revision_author" << vcs::name << endl;
    cout << setw(width) << "vcs::revision_author_name" << vcs::revision_author_name << endl;
    cout << setw(width) << "vcs::revision_author_email" << vcs::revision_author_email << endl;
    cout << setw(width) << "vcs::revision_message" << vcs::revision_message << endl;
    cout << setw(width) << "vcs::revision_timestamp" << vcs::revision_timestamp << endl;
    cout << setw(width) << "vcs::revision_time_rfc2822" << vcs::revision_time_rfc2822 << endl;
    cout << setw(width) << "vcs::revision_tags";
    for(auto&& x : vcs::revision_tags)
    	cout << x << ", ";
    cout << endl;

    cout << setw(width) << "station::node" << station::node << endl;
    cout << setw(width) << "station::user" << station::user << endl;
    cout << setw(width) << "station::arch" << station::arch << endl;
    cout << setw(width) << "station::system" << station::system << endl;
    cout << setw(width) << "station::system_version" << station::system_version << endl;
    cout << setw(width) << "station::timestamp" << station::timestamp << endl;
    cout << setw(width) << "station::time_rfc2822" << station::time_rfc2822 << endl;

    cout << setw(width) << "build::toolchain" << build::toolchain << endl;
    cout << setw(width) << "build::toolchain_version" << build::toolchain_version << endl;
    cout << setw(width) << "build::target_system" << build::target_system << endl;
    cout << setw(width) << "build::target_arch" << build::target_arch << endl;
}
