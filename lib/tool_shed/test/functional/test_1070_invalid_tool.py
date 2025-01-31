from ..base.twilltestcase import (
    common,
    ShedTwillTestCase,
)

repository_name = "bismark_0070"
repository_description = "Galaxy's bismark wrapper"
repository_long_description = "Long description of Galaxy's bismark wrapper"
category_name = "Test 0070 Invalid Tool Revisions"
category_description = "Test 1070 for a repository with an invalid tool."


class TestFreebayesRepository(ShedTwillTestCase):
    """Test repository with multiple revisions with invalid tools."""

    def test_0000_create_or_login_admin_user(self):
        """Create necessary user accounts and login as an admin user."""
        self.galaxy_login(email=common.admin_email, username=common.admin_username)
        self.login(email=common.test_user_1_email, username=common.test_user_1_name)
        self.login(email=common.admin_email, username=common.admin_username)

    def test_0005_ensure_existence_of_repository_and_category(self):
        """Create freebayes repository and upload only freebayes.xml. This should result in an error message and invalid tool."""
        self.create_category(name=category_name, description=category_description)
        self.login(email=common.test_user_1_email, username=common.test_user_1_name)
        category = self.populator.get_category_with_name(category_name)
        repository = self.get_or_create_repository(
            name=repository_name,
            description=repository_description,
            long_description=repository_long_description,
            owner=common.test_user_1_name,
            category=category,
            strings_displayed=[],
        )
        if self.repository_is_new(repository):
            self.upload_file(
                repository,
                filename="bismark/bismark.tar",
                filepath=None,
                valid_tools_only=False,
                uncompress_file=True,
                remove_repo_files_not_in_tar=False,
                commit_message="Uploaded bismark tarball.",
                strings_displayed=[],
                strings_not_displayed=[],
            )
            self.upload_file(
                repository,
                filename="bismark/bismark_methylation_extractor.xml",
                filepath=None,
                valid_tools_only=False,
                uncompress_file=False,
                remove_repo_files_not_in_tar=False,
                commit_message="Uploaded an updated tool xml.",
                strings_displayed=[],
                strings_not_displayed=[],
            )

    def test_0010_browse_tool_shed(self):
        """Browse the available tool sheds in this Galaxy instance and preview the bismark repository."""
        self.galaxy_login(email=common.admin_email, username=common.admin_username)
        self.browse_tool_shed(url=self.url, strings_displayed=[category_name])
        category = self.populator.get_category_with_name(category_name)
        self.browse_category(category, strings_displayed=[repository_name])
        self.preview_repository_in_tool_shed(
            repository_name, common.test_user_1_name, strings_displayed=[repository_name]
        )

    def test_0015_install_freebayes_repository(self):
        """Install the test repository without installing tool dependencies."""
        self.install_repository(
            repository_name,
            common.test_user_1_name,
            category_name,
            install_tool_dependencies=False,
            new_tool_panel_section_label="test_1070",
        )
        installed_repository = self.test_db_util.get_installed_repository_by_name_owner(
            repository_name, common.test_user_1_name
        )
        strings_displayed = [
            "bismark_0070",
            "Galaxy's bismark wrapper",
            "user1",
            self.url.replace("http://", ""),
            installed_repository.installed_changeset_revision,
        ]
        self.display_galaxy_browse_repositories_page(strings_displayed=strings_displayed)
        strings_displayed.extend(["methylation extractor", "Invalid tools"])
        self.display_installed_repository_manage_page(
            installed_repository, strings_displayed=strings_displayed, strings_not_displayed=["bisulfite mapper"]
        )
        self.verify_tool_metadata_for_installed_repository(installed_repository)
        self.update_installed_repository_api(installed_repository, verify_no_updates=True)
        assert "invalid_tools" in installed_repository.metadata_, (
            "No invalid tools were defined in %s." % installed_repository.name
        )
