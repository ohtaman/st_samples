import time

import job_queue


def run():
    while True:
        job_id, args = job_queue.get_job()
        # Long process
        time.sleep(20)
        # Do something
        result = sum(args)
        # save result
        job_queue.save_artifact(
            job_id=job_id,
            name='result',
            data={'result': result}
        )


def main():
    run()


if __name__ == '__main__':
    main()