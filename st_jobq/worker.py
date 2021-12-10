import time

import job_queue


def run():
    while True:
        job_id, args = job_queue.get_job()
        # Long process
        time.sleep(10)
        # Do something
        result = sum(args)
        # save result
        job_queue.save_artifact(
            job_id=job_id,
            name='result',
            data={
                'a': args[0],
                'b': args[1],
                'sum': result
            }
        )


def main():
    run()


if __name__ == '__main__':
    main()