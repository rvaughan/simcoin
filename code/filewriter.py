import config
import logging
import json
import time
from parse import ReceivedEvent
from parse import BlockEvent
from parse import TxEvent
from systemmonitor import CpuTimeSnapshot
from systemmonitor import MemorySnapshot
from clistats import Tip
import utils
from runner import StepTimes


class FileWriter:
    def __init__(self, context):
        self.context = context
        self.args = utils.read_json_file(config.args_json)

    def execute(self):
        utils.write_csv(self.context.path.blocks_csv, BlockEvent.csv_header(), self.context.parsed_blocks.values(), self.args.tag)
        utils.write_csv(self.context.path.txs_csv, TxEvent.csv_header(), self.context.parsed_txs.values(), self.args.tag)
        utils.write_csv(self.context.path.blocks_received_csv, ReceivedEvent.csv_header(), self.context.blocks_received, self.args.tag)
        utils.write_csv(self.context.path.txs_received_csv, ReceivedEvent.csv_header(), self.context.txs_received, self.args.tag)
        utils.write_csv(self.context.path.tips_csv, Tip.csv_header(), self.context.tips, self.args.tag)
        utils.write_csv(self.context.path.cpu_time_csv, CpuTimeSnapshot.csv_header(), self.context.cpu_time, self.args.tag)
        utils.write_csv(self.context.path.memory_csv, MemorySnapshot.csv_header(), self.context.memory, self.args.tag)

        self.create_general_infos_json()

        self.context.step_times.append(StepTimes(time.time(), 'postprocessing_end'))
        utils.write_csv(self.context.path.step_times, StepTimes.csv_header(), self.context.step_times, self.args.tag)

        logging.info('Executed analyzer')

    def create_general_infos_json(self):
        with open(self.context.path.general_infos_json, 'w') as file:
            file.write('{}\n'.format(json.dumps(self.context.general_infos)))
