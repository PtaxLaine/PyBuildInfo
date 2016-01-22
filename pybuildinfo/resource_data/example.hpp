#pragma once
#ifndef BUILDINFO_H
#define BUILDINFO_H
#include <cinttypes>
#include <ctime>
#include <string>

namespace BuildInfo{
    static const ::std::string scm_name             = "$scm_name$";
    static const ::std::string scm_branch           = "$scm_branch$";
    static const ::std::string scm_revisions        = "$scm_revisions$";
    static const ::std::string scm_revisions_short  = "$scm_revisions_short$";
    static const ::std::string scm_version          = "$scm_version$";
    static const ::std::string scm_version_tags     = "$scm_version_tags$";
    static const bool          scm_version_stable   = static_cast<bool>($scm_version_stable$ul);
    static const ::uint32_t    scm_version_major    = $scm_version_major$ul;
    static const ::uint32_t    scm_version_minor    = $scm_version_minor$ul;
    static const ::uint32_t    scm_version_patch    = $scm_version_patch$ul;
    static const ::std::string scm_author           = "$scm_author$";
    static const ::std::string scm_author_email     = "$scm_author_email$";
    static const ::std::string scm_message_escaping = "$scm_message_escaping$";
    static const ::std::string scm_rfc2822          = "$scm_rfc2822$";
    static const ::time_t      scm_timestamp        = $scm_timestamp$ull;

    static const ::std::string build_system         = "$build_system$";
    static const ::std::string build_system_version = "$build_system_version$";
    static const ::std::string build_machine        = "$build_machine$";
    static const ::std::string build_node           = "$build_node$";
    static const ::std::string build_node_login     = "$build_node_login$";
    static const ::time_t      build_timestamp      = $build_time$ull;
    static const ::std::string build_rfc2822        = "$build_rfc2822$";

    static const ::std::string build_toolchain         = "$build_toolchain$";
    static const ::std::string build_toolchain_version = "$build_toolchain_version$";
    static const ::std::string build_target_system     = "$build_target_system$";
    static const ::std::string build_target_machine    = "$build_target_machine$";
}
#endif
