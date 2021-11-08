from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = "#358140"
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        IGNOREHEADER {}
        DELIMITER '{}'
    """
    copy_sql_with_json_path = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        JSON '{}'
    """
    
    template_fields = ("s3_file_key",)

    @apply_defaults
    def __init__(
        self,
        s3_bucket,
        s3_file_key,
        target_table_name,
        aws_conn_id="aws_credentials",
        redshift_conn_id="redshift",
        ignore_headers=1,
        delimiter=",",
        json_path=None,
        *args,
        **kwargs,
    ):
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.s3_bucket = s3_bucket
        self.s3_file_key = s3_file_key
        self.target_table_name = target_table_name
        self.redshift_conn_id = redshift_conn_id
        self.aws_conn_id = aws_conn_id
        self.ignore_headers = ignore_headers
        self.delimiter = delimiter
        self.json_path = json_path

    def execute(self, context):
        aws_hook = AwsHook(aws_conn_id=self.aws_conn_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Copying data from S3 to Redshift")
        rendered_s3_key = self.s3_file_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_s3_key)
        if self.json_path:
            formatted_query = StageToRedshiftOperator.copy_sql_with_json_path.format(
                f"public.{self.target_table_name}",
                s3_path,
                credentials.access_key,
                credentials.secret_key,
                self.json_path
            )
        else:
            formatted_query = StageToRedshiftOperator.copy_sql.format(
                f"public.{self.target_table_name}",
                s3_path,
                credentials.access_key,
                credentials.secret_key,
                self.ignore_headers,
                self.delimiter,
            )
        redshift.run(formatted_query)



