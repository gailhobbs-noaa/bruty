-- Function: automatically set enc_request_pause_at
-- whenever enc_request_pause changes from not-TRUE to TRUE.

CREATE OR REPLACE FUNCTION public.set_enc_request_pause_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.enc_request_pause = TRUE
       AND OLD.enc_request_pause IS DISTINCT FROM TRUE THEN

        NEW.enc_request_pause_at = clock_timestamp();
    END IF;

    RETURN NEW;
END;
$$;


-- Recreate the trigger safely if this script is run again.

DROP TRIGGER IF EXISTS trg_set_enc_request_pause_at
ON public.bruty_status_dev;


CREATE TRIGGER trg_set_enc_request_pause_at
BEFORE UPDATE OF enc_request_pause
ON public.bruty_status_dev
FOR EACH ROW
EXECUTE FUNCTION public.set_enc_request_pause_at();
