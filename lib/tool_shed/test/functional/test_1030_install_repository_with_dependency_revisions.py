from ..base.twilltestcase import (
    common,
    ShedTwillTestCase,
)

column_maker_repository_name = "column_maker_0030"
column_maker_repository_description = "A flexible aligner."
column_maker_repository_long_description = "A flexible aligner and methylation caller for Bisulfite-Seq applications."

emboss_repository_name = "emboss_0030"
emboss_5_repository_name = "emboss_5_0030"
emboss_6_repository_name = "emboss_6_0030"
emboss_repository_description = "Galaxy wrappers for Emboss version 5.0.0 tools for test 0030"
emboss_repository_long_description = "Galaxy wrappers for Emboss version 5.0.0 tools for test 0030"

running_standalone = False


class RepositoryWithDependencyRevisions(ShedTwillTestCase):
    """Test installing a repository with dependency revisions."""

    def test_0000_initiate_users(self):
        """Create necessary user accounts."""
        self.login(email=common.test_user_1_email, username=common.test_user_1_name)
        self.login(email=common.admin_email, username=common.admin_username)
        self.galaxy_login(email=common.admin_email, username=common.admin_username)

    def test_0005_ensure_repositories_and_categories_exist(self):
        """Create the 0030 category and add repositories to it, if necessary."""
        global running_standalone
        category = self.create_category(
            name="Test 0030 Repository Dependency Revisions", description="Test 0030 Repository Dependency Revisions"
        )
        self.login(email=common.test_user_1_email, username=common.test_user_1_name)
        column_maker_repository = self.get_or_create_repository(
            name=column_maker_repository_name,
            description=column_maker_repository_description,
            long_description=column_maker_repository_long_description,
            owner=common.test_user_1_name,
            category=category,
            strings_displayed=[],
        )
        if self.repository_is_new(column_maker_repository):
            running_standalone = True
            self.upload_file(
                column_maker_repository,
                filename="column_maker/column_maker.tar",
                filepath=None,
                valid_tools_only=True,
                uncompress_file=True,
                remove_repo_files_not_in_tar=False,
                commit_message="Uploaded column_maker tarball.",
                strings_displayed=[],
                strings_not_displayed=[],
            )
            emboss_5_repository = self.get_or_create_repository(
                name=emboss_5_repository_name,
                description=emboss_repository_description,
                long_description=emboss_repository_long_description,
                owner=common.test_user_1_name,
                category=category,
                strings_displayed=[],
            )
            self.upload_file(
                emboss_5_repository,
                filename="emboss/emboss.tar",
                filepath=None,
                valid_tools_only=True,
                uncompress_file=False,
                remove_repo_files_not_in_tar=False,
                commit_message="Uploaded tool tarball.",
                strings_displayed=[],
                strings_not_displayed=[],
            )
            repository_dependencies_path = self.generate_temp_path("test_1030", additional_paths=["emboss", "5"])
            column_maker_tuple = (
                self.url,
                column_maker_repository.name,
                column_maker_repository.owner,
                self.get_repository_tip(column_maker_repository),
            )
            self.create_repository_dependency(
                repository=emboss_5_repository,
                repository_tuples=[column_maker_tuple],
                filepath=repository_dependencies_path,
            )
            emboss_6_repository = self.get_or_create_repository(
                name=emboss_6_repository_name,
                description=emboss_repository_description,
                long_description=emboss_repository_long_description,
                owner=common.test_user_1_name,
                category=category,
                strings_displayed=[],
            )
            self.upload_file(
                emboss_6_repository,
                filename="emboss/emboss.tar",
                filepath=None,
                valid_tools_only=True,
                uncompress_file=False,
                remove_repo_files_not_in_tar=False,
                commit_message="Uploaded tool tarball.",
                strings_displayed=[],
                strings_not_displayed=[],
            )
            repository_dependencies_path = self.generate_temp_path("test_1030", additional_paths=["emboss", "6"])
            column_maker_tuple = (
                self.url,
                column_maker_repository.name,
                column_maker_repository.owner,
                self.get_repository_tip(column_maker_repository),
            )
            self.create_repository_dependency(
                repository=emboss_6_repository,
                repository_tuples=[column_maker_tuple],
                filepath=repository_dependencies_path,
            )
            emboss_repository = self.get_or_create_repository(
                name=emboss_repository_name,
                description=emboss_repository_description,
                long_description=emboss_repository_long_description,
                owner=common.test_user_1_name,
                category=category,
                strings_displayed=[],
            )
            self.upload_file(
                emboss_repository,
                filename="emboss/emboss.tar",
                filepath=None,
                valid_tools_only=True,
                uncompress_file=False,
                remove_repo_files_not_in_tar=False,
                commit_message="Uploaded tool tarball.",
                strings_displayed=[],
                strings_not_displayed=[],
            )
            repository_dependencies_path = self.generate_temp_path("test_1030", additional_paths=["emboss", "5"])
            dependency_tuple = (
                self.url,
                emboss_5_repository.name,
                emboss_5_repository.owner,
                self.get_repository_tip(emboss_5_repository),
            )
            self.create_repository_dependency(
                repository=emboss_repository,
                repository_tuples=[dependency_tuple],
                filepath=repository_dependencies_path,
            )
            dependency_tuple = (
                self.url,
                emboss_6_repository.name,
                emboss_6_repository.owner,
                self.get_repository_tip(emboss_6_repository),
            )
            self.create_repository_dependency(
                repository=emboss_repository,
                repository_tuples=[dependency_tuple],
                filepath=repository_dependencies_path,
            )

    def test_0010_browse_tool_shed(self):
        """Browse the available tool sheds in this Galaxy instance and preview the emboss tool."""
        self.galaxy_login(email=common.admin_email, username=common.admin_username)
        self.browse_tool_shed(url=self.url, strings_displayed=["Test 0030 Repository Dependency Revisions"])
        category = self.populator.get_category_with_name("Test 0030 Repository Dependency Revisions")
        self.browse_category(category, strings_displayed=["emboss_0030"])
        self.preview_repository_in_tool_shed(
            "emboss_0030", common.test_user_1_name, strings_displayed=["emboss_0030", "Valid tools"]
        )

    def test_0015_install_emboss_repository(self):
        """Install the emboss repository without installing tool dependencies."""
        global running_standalone
        self.install_repository(
            "emboss_0030",
            common.test_user_1_name,
            "Test 0030 Repository Dependency Revisions",
            install_tool_dependencies=False,
            new_tool_panel_section_label="test_1030",
        )
        installed_repository = self.test_db_util.get_installed_repository_by_name_owner(
            "emboss_0030", common.test_user_1_name
        )
        strings_displayed = [
            "emboss_0030",
            "Galaxy wrappers for Emboss version 5.0.0 tools for test 0030",
            "user1",
            self.url.replace("http://", ""),
            installed_repository.installed_changeset_revision,
        ]
        self.display_galaxy_browse_repositories_page(strings_displayed=strings_displayed)
        strings_displayed.extend(["Installed tool shed repository", "Valid tools", "antigenic"])
        self.display_installed_repository_manage_page(installed_repository, strings_displayed=strings_displayed)
        self.verify_tool_metadata_for_installed_repository(installed_repository)
        self.update_installed_repository_api(installed_repository, verify_no_updates=True)

    def test_0025_verify_installed_repository_metadata(self):
        """Verify that resetting the metadata on an installed repository does not change the metadata."""
        self.verify_installed_repository_metadata_unchanged("emboss_0030", common.test_user_1_name)
