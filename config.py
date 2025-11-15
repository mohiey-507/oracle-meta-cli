METADATA_QUERIES = {
    'TABLE': {
        'columns': """
            SELECT column_name, data_type, data_length, nullable
            FROM all_tab_columns
            WHERE table_name = :object_name
            ORDER BY column_id
        """,
        'constraints': """
            SELECT constraint_name, constraint_type, search_condition, r_constraint_name
            FROM all_constraints
            WHERE table_name = :object_name
            ORDER BY constraint_name
        """,
        'indexes': """
            SELECT index_name, index_type, uniqueness
            FROM all_indexes
            WHERE table_name = :object_name
            ORDER BY index_name
        """,
        'triggers': """
            SELECT trigger_name, trigger_type, triggering_event, status
            FROM all_triggers
            WHERE table_name = :object_name
            ORDER BY trigger_name
        """
    },
    'VIEW': {
        'columns': """
            SELECT column_name, data_type, data_length, nullable
            FROM all_tab_columns
            WHERE table_name = :object_name
            ORDER BY column_id
        """,
        'text': """
            SELECT text
            FROM all_views
            WHERE view_name = :object_name
        """
    },
    'SEQUENCE': {
        'details': """
            SELECT sequence_name, min_value, max_value, increment_by, last_number
            FROM all_sequences
            WHERE sequence_name = :object_name
        """
    },
    'CONSTRAINT': {
        'details': """
            SELECT constraint_name, constraint_type, table_name, search_condition, r_constraint_name
            FROM all_constraints
            WHERE constraint_name = :object_name
        """
    },
    'USER': {
        'details': """
            SELECT username, user_id, created
            FROM all_users
            WHERE username = :object_name
        """
    }
}

OBJECT_LIST_QUERIES = {
    'TABLE': "SELECT table_name FROM user_tables ORDER BY table_name",
    'VIEW': "SELECT view_name FROM user_views ORDER BY view_name",
    'SEQUENCE': "SELECT sequence_name FROM user_sequences ORDER BY sequence_name",
    'CONSTRAINT': "SELECT constraint_name FROM user_constraints ORDER BY constraint_name",
    'USER': "SELECT username FROM all_users ORDER BY username"
}
