<%namespace file="/webapps/tool_shed/common/common.mako" import="*" />
<%namespace file="/webapps/tool_shed/repository/common.mako" import="*" />

<%def name="browse_files(title_text, directory_path)">
    <script type="text/javascript">
        config.addInitialization(function() {
            console.log("common.mako, browse_files");

            // --- Initialize sample trees
            $("#tree").dynatree({
                title: "${title_text|h}",
                minExpandLevel: 1,
                persist: false,
                checkbox: true,
                selectMode: 3,
                onPostInit: function(isReloading, isError) {
                    // Re-fire onActivate, so the text is updated
                    this.reactivate();
                },
                fx: { height: "toggle", duration: 200 },
                // initAjax is hard to fake, so we pass the children as object array:
                initAjax: {url: "${h.url_for( controller='admin_toolshed', action='open_folder' )}",
                           dataType: "json",
                           data: { folder_path: "${directory_path|h}",
                                   repository_id: "${trans.security.encode_id( repository.id )}" },
                },
                onLazyRead: function(dtnode){
                    dtnode.appendAjax({
                        url: "${h.url_for( controller='admin_toolshed', action='open_folder' )}",
                        dataType: "json",
                        data: { folder_path: dtnode.data.key,
                                repository_id: "${trans.security.encode_id( repository.id )}" },
                    });
                },
                onSelect: function(select, dtnode) {
                    // Display list of selected nodes
                    var selNodes = dtnode.tree.getSelectedNodes();
                    // convert to title/key array
                    var selKeys = $.map(selNodes, function(node) {
                        return node.data.key;
                    });
                },
                onActivate: function(dtnode) {
                    var cell = $("#file_contents");
                    var selected_value;
                     if (dtnode.data.key == 'root') {
                        selected_value = "${directory_path|h}/";
                    } else {
                        selected_value = dtnode.data.key;
                    };
                    if (selected_value.charAt(selected_value.length-1) != '/') {
                        // Make ajax call
                        $.ajax( {
                            type: "POST",
                            url: "${h.url_for( controller='admin_toolshed', action='get_file_contents' )}",
                            dataType: "json",
                            data: { file_path: selected_value, repository_id: "${trans.security.encode_id( repository.id )}" },
                            success : function( data ) {
                                cell.html( '<label>'+data+'</label>' )
                            }
                        });
                    } else {
                        cell.html( '' );
                    };
                },
            });
        });
    </script>
</%def>

<%def name="render_dependencies_section( install_resolver_dependencies_check_box, repository_dependencies_check_box, containers_dict, revision_label=None, export=False, requirements_status=None )">
    <style type="text/css">
        #dependency_table{ table-layout:fixed;
                           width:100%;
                           overflow-wrap:normal;
                           overflow:hidden;
                           border:0px;
                           word-break:keep-all;
                           word-wrap:break-word;
                           line-break:strict; }
    </style>
    <script type="text/javascript">
         config.addInitialization(function() {
             console.log("common.mako, render_dependencies_section");

             $(".detail-section").hide();
             var hidden = true;
             $(".toggle-detail-section").click(function(e){
                 e.preventDefault();
                 hidden = !hidden;
                 if (hidden === true){
                     $(".toggle-detail-section").text('Display Details');
                 } else{
                     $(".toggle-detail-section").text('Hide Details');
                 }
                 $(".detail-section").toggle();
             })
         });
     </script>
    <%
        from markupsafe import escape
        class RowCounter( object ):
            def __init__( self ):
                self.count = 0
            def increment( self ):
                self.count += 1
            def __str__( self ):
                return str( self.count )

        repository_dependencies_root_folder = containers_dict.get( 'repository_dependencies', None )
        missing_repository_dependencies_root_folder = containers_dict.get( 'missing_repository_dependencies', None )
        tool_dependencies_root_folder = containers_dict.get( 'tool_dependencies', None )
        missing_tool_dependencies_root_folder = containers_dict.get( 'missing_tool_dependencies', None )
        env_settings_heaader_row_displayed = False
        package_header_row_displayed = False
        if revision_label:
            revision_label_str = ' revision <b>%s</b> of ' % escape( str( revision_label ) )
        else:
            revision_label_str = ' '
    %>
    <div class="form-row">
        <p>
            By default Galaxy will install all needed dependencies for${revision_label_str}the repository. See the
            <a target="_blank" href="https://docs.galaxyproject.org/en/master/admin/dependency_resolvers.html">
                dependency resolver documentation
            </a>.
        </p>
        <p>
            You can control how dependencies are installed (this is an advanced option, if in doubt, use the default)
            <button class="toggle-detail-section">
                Display Details
            </button>
        </p>
        <p>
        </p>
     </div>
   %if export:
    <div class="form-row">
        <div class="toolParamHelp" style="clear: both;">
            <p>
                The following additional repositories are required by${revision_label_str}the <b>${repository.name|h}</b> repository and they can be exported as well.
            </p>
        </div>
    </div>
    %endif
    <div style="clear: both"></div>
    <div class="detail-section">
    %if repository_dependencies_root_folder or missing_repository_dependencies_root_folder:
        %if repository_dependencies_check_box:
            <div class="form-row">
                %if export:
                    <label>Export repository dependencies?</label>
                %else:
                    <label>Handle repository dependencies?</label>
                %endif
                ${render_checkbox(repository_dependencies_check_box)}
                <div class="toolParamHelp" style="clear: both;">
                    %if export:
                        Select to export the following additional repositories that are required by this repository.
                    %else:
                        Select to automatically install these additional Tool Shed repositories required by this repository.
                    %endif
                </div>
            </div>
            <div style="clear: both"></div>
        %endif
        %if repository_dependencies_root_folder:
            <div class="form-row">
                <p/>
                <% row_counter = RowCounter() %>
                <table cellspacing="2" cellpadding="2" border="0" width="100%" class="tables container-table">
                    ${render_folder( repository_dependencies_root_folder, 0, parent=None, row_counter=row_counter, is_root_folder=True )}
                </table>
                <div style="clear: both"></div>
            </div>
        %endif
        %if missing_repository_dependencies_root_folder:
            <div class="form-row">
                <p/>
                <% row_counter = RowCounter() %>
                <table cellspacing="2" cellpadding="2" border="0" width="100%" class="tables container-table">
                    ${render_folder( missing_repository_dependencies_root_folder, 0, parent=None, row_counter=row_counter, is_root_folder=True )}
                </table>
                <div style="clear: both"></div>
            </div>
        %endif
    %endif
    %if tool_dependencies_root_folder or missing_tool_dependencies_root_folder:
        %if tool_dependencies_root_folder:
            <div class="form-row">
                <p/>
                <% row_counter = RowCounter() %>
                <table cellspacing="2" cellpadding="2" border="0" width="100%" class="tables container-table" id="dependency_table">
                    ${render_folder( tool_dependencies_root_folder, 0, parent=None, row_counter=row_counter, is_root_folder=True )}
                </table>
                <div style="clear: both"></div>
            </div>
        %endif
        %if missing_tool_dependencies_root_folder:
            <div class="form-row">
                <p/>
                <% row_counter = RowCounter() %>
                <table cellspacing="2" cellpadding="2" border="0" width="100%" class="tables container-table" id="dependency_table">
                    ${render_folder( missing_tool_dependencies_root_folder, 0, parent=None, row_counter=row_counter, is_root_folder=True )}
                </table>
                <div style="clear: both"></div>
            </div>
        %endif
    </div>
    %endif
    <div style="clear: both"></div>
    %if requirements_status and install_resolver_dependencies_check_box:
    <div class="form-row">
        <label>When available, install <a href="https://docs.galaxyproject.org/en/master/admin/conda_faq.html" target="_blank">Conda</a> managed tool dependencies?</label>
        ${render_checkbox(install_resolver_dependencies_check_box)}
        <div class="toolParamHelp" style="clear: both;">
            Select to automatically install tool dependencies via Conda.
        </div>
    </div>
    %endif
    </div>
</%def>

<%def name="render_readme_section( containers_dict )">
    <%
        class RowCounter( object ):
            def __init__( self ):
                self.count = 0
            def increment( self ):
                self.count += 1
            def __str__( self ):
                return str( self.count )

        readme_files_root_folder = containers_dict.get( 'readme_files', None )
    %>
    %if readme_files_root_folder:
        <p/>
        <div class="form-row">
            <% row_counter = RowCounter() %>
            <table cellspacing="2" cellpadding="2" border="0" width="100%" class="tables container-table">
                ${render_folder( readme_files_root_folder, 0, parent=None, row_counter=row_counter, is_root_folder=True )}
            </table>
        </div>
    %endif
</%def>

