from worker_deploy import deploy


def main():
    """
    the main deploy_worker.txt all the program on the machine
    the import the worker_main
    the run it
    you must delay the because worker_main is depended on the deploy_worker.txt phase
    :return: None
    """
    deploy()
    from workers.worker import worker_main
    worker_main()


if __name__ == "__main__":
    main()