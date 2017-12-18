mod buildinfo;

macro_rules! printbuidinfo {
    ($x:path) => (
    {
        println!("{:<32}{}", stringify!($x), $x);
    }
    );
}

fn print_test(){
    use buildinfo::*;
    printbuidinfo!(vcs::name);
    printbuidinfo!(vcs::revision);
    printbuidinfo!(vcs::revision_short);
    printbuidinfo!(vcs::revision_version);
    printbuidinfo!(vcs::revision_version_tag);
    printbuidinfo!(vcs::revision_version_major);
    printbuidinfo!(vcs::revision_version_minor);
    printbuidinfo!(vcs::revision_version_patch);
    printbuidinfo!(vcs::revision_version_stable);
    printbuidinfo!(vcs::revision_author);
    printbuidinfo!(vcs::revision_author_name);
    printbuidinfo!(vcs::revision_author_email);
    printbuidinfo!(vcs::revision_message);
    printbuidinfo!(vcs::revision_timestamp);
    printbuidinfo!(vcs::revision_time_rfc2822);

    printbuidinfo!(station::node);
    printbuidinfo!(station::user);
    printbuidinfo!(station::arch);
    printbuidinfo!(station::system);
    printbuidinfo!(station::system_version);
    printbuidinfo!(station::timestamp);
    printbuidinfo!(station::time_rfc2822);

    printbuidinfo!(build::compiler);
    printbuidinfo!(build::version);
    printbuidinfo!(build::target);
}

fn main() {
    print_test();
}

#[test]
fn test() {
    print_test();
}
