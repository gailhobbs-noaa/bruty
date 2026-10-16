from nbs.bruty.nbs_postgres import (
    connect_params_from_config,
    connection_with_retries,
)


def get_enc_request_pause(config, pid):
    conn_info = connect_params_from_config(config)
    conn_info.database = config.get('export_database')

    connection, cursor = connection_with_retries(conn_info)

    cursor.execute(
        """
        SELECT enc_request_pause
        FROM public.bruty_status
        WHERE pid = %s
        """,
        (pid,)
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return False if row is None else row[0]


def update_is_paused(config, pid, is_paused):
    conn_info = connect_params_from_config(config)
    conn_info.database = config.get('export_database')

    connection, cursor = connection_with_retries(conn_info)

    if is_paused:
        cursor.execute(
            """
            UPDATE public.bruty_status
            SET is_paused = TRUE,
                is_paused_at = clock_timestamp()
            WHERE pid = %s
            """,
            (pid,)
        )
    else:
        cursor.execute(
            """
            UPDATE public.bruty_status
            SET is_paused = FALSE
            WHERE pid = %s
            """,
            (pid,)
        )

    connection.commit()
    cursor.close()
    connection.close()

def update_progress(config, pid, progress):
    progress = max(0, min(100, int(progress)))

    conn_info = connect_params_from_config(config)
    conn_info.database = config.get('export_database')

    connection, cursor = connection_with_retries(conn_info)

    cursor.execute(
        """
        UPDATE public.bruty_status
        SET progress = %s
        WHERE pid = %s
        """,
        (progress, pid)
    )

    connection.commit()
    cursor.close()
    connection.close()