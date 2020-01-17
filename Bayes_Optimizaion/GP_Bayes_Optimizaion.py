#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/7 1:21 PM
# @Author  : Slade
# @File    : GP_Bayes_Optimizaion.py

import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern


class GP_Bayes_Optimizaion:
    def __init__(self):
        self.init_point_number = 3
        self.acquisition_function_kappa = 5
        self.iteration_number = 50

    def target_loss_function(self, x):
        '''
        这边援引的是：https://blog.csdn.net/Leon_winter/article/details/86604553 需要解决的问题，其实我们已经解在2左右，max_value是1.4
        除此之外，可以用random forest的N则交叉的AUC的均值为loss，或者MLE的公式，都可以
        :param x:
        :return:
        '''
        return np.exp(-(x - 2) ** 2) + np.exp(-(x - 6) ** 2 / 10) + 1 / (x ** 2 + 1)

    def Acquision_function(self, mean, std):
        return mean + self.acquisition_function_kappa * std

    def model(self):
        iteration_index = 0
        train_features = []
        train_negative_loss = []

        # Matern核,不同的核衡量X之间的相似度不一致，高斯过程中的协方差不一致
        # 每次进行25次采样
        gp = GaussianProcessRegressor(
            kernel=Matern(nu=2.5),
            n_restarts_optimizer=25, )

        bound_dict = {'x': (-4, 4), 'y': (-3, 3)}
        bounds = []
        for k, item in bound_dict.items():
            bounds.append(item)
        bounds = np.asarray(bounds)
        # 初始化
        init_xs = np.random.uniform(bound_dict.get("x", [0, 0])[0], bound_dict.get("x", [1, 1])[1],
                                    size=self.init_point_number)
        init_ys = np.random.uniform(bound_dict.get("y", [0, 0])[0], bound_dict.get("y", [1, 1])[1],
                                    size=self.init_point_number)
        init_points = zip(init_xs, init_ys)
        init_labels = map(self.target_loss_function, init_xs)
        train_features = np.asarray(list(init_points))
        train_negative_loss = np.asarray(list(init_labels))
        current_max_negative_loss = max(train_negative_loss)

        # GP
        gp.fit(train_features, train_negative_loss)

        # Acquision function computes the max value
        x_tries = np.random.uniform(
            bounds[:, 0], bounds[:, 1], size=(100000, bounds.shape[0]))
        mean, std = gp.predict(x_tries, return_std=True)
        acquisition_fucntion_values = self.Acquision_function(mean, std)
        x_max = x_tries[np.argmax(acquisition_fucntion_values)]
        max_acquision_fucntion_value = max(acquisition_fucntion_values)
        x_max = np.clip(x_max, bounds[:, 0], bounds[:, 1])
        print("Current Max Acquision Function Choose: {}".format(x_max))

        for i in range(self.iteration_number):
            iteration_index += 1

            # Choose the best and compute to add in train dataset
            train_features = np.vstack((train_features, x_max.reshape((1, -1))))
            train_negative_loss = np.append(train_negative_loss,
                                            self.target_loss_function(x_max[0]))

            # Re-compute gaussian process and acquistion function
            gp.fit(train_features, train_negative_loss)

            # Update maximum value
            if train_negative_loss[-1] > current_max_negative_loss:
                current_max_negative_loss = train_negative_loss[-1]
                print("Get The Better Parameters,The Better Parameters is {}".format(current_max_negative_loss))

            x_tries = np.random.uniform(
                bounds[:, 0], bounds[:, 1], size=(100000, bounds.shape[0]))

            mean, std = gp.predict(x_tries, return_std=True)
            acquisition_fucntion_values = mean + self.acquisition_function_kappa * std
            x_max = x_tries[acquisition_fucntion_values.argmax()]
            max_acquision_fucntion_value = acquisition_fucntion_values.max()

            x_max = np.clip(x_max, bounds[:, 0], bounds[:, 1])
            print("Max Negative Loss: {}, Current Negative Loss: {}, Acquision Function Choose: {}".
                  format(current_max_negative_loss, train_negative_loss[-1], x_max))
        return (current_max_negative_loss, train_negative_loss[-1], x_max, max_acquision_fucntion_value)


if __name__ == '__main__':
    gpbo = GP_Bayes_Optimizaion()
    print(gpbo.model())
    '''
    Current Max Acquision Function Choose: [ 3.97180086 -2.99972585]
    Max Negative Loss: 1.048945269700466, Current Negative Loss: 0.7428469513803806, Acquision Function Choose: [3.99810821 2.98117431]
    Max Negative Loss: 1.048945269700466, Current Negative Loss: 0.7471433841787855, Acquision Function Choose: [-3.99216178 -2.99784479]
    Max Negative Loss: 1.048945269700466, Current Negative Loss: 0.05908721033758831, Acquision Function Choose: [ 3.99805917e+00 -3.82496481e-03]
    Max Negative Loss: 1.048945269700466, Current Negative Loss: 0.7471352082187401, Acquision Function Choose: [ 0.87877575 -2.99587744]
    Max Negative Loss: 1.048945269700466, Current Negative Loss: 0.9213278545195327, Acquision Function Choose: [-3.99397523  2.99299499]
    Max Negative Loss: 1.048945269700466, Current Negative Loss: 0.05903660305525495, Acquision Function Choose: [1.17362324 2.99991327]
    Max Negative Loss: 1.048945269700466, Current Negative Loss: 1.0231347368200185, Acquision Function Choose: [ 2.0422064  -1.22679432]
    Get The Better Parameters,The Better Parameters is 1.4004138739293137
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 1.4004138739293137, Acquision Function Choose: [2.15550625 1.07557761]
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 1.3813082997417614, Acquision Function Choose: [ 1.89756555 -0.105417  ]
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 1.3927339492495443, Acquision Function Choose: [-3.99656643 -0.21319406]
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 0.05896440187671829, Acquision Function Choose: [ 1.12212638 -1.32364188]
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 0.9979568757258983, Acquision Function Choose: [-1.51354468 -2.99990393]
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 0.30741417552734474, Acquision Function Choose: [-1.16188992  2.9992418 ]
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 0.43150046496220545, Acquision Function Choose: [ 2.50057685 -2.9838008 ]
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 1.2101039105334932, Acquision Function Choose: [ 3.23867259 -1.6002495 ]
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 0.7691462593539511, Acquision Function Choose: [0.78426374 1.55826202]
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 0.9131074714523291, Acquision Function Choose: [2.59456073 2.99752356]
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 1.1451408858987413, Acquision Function Choose: [3.49662732 1.57079087]
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 0.7164351568119892, Acquision Function Choose: [-2.36798507 -1.2757943 ]
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 0.15225630744796492, Acquision Function Choose: [2.79883998 0.01415101]
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 1.0003654883378552, Acquision Function Choose: [-2.84407322  1.5097039 ]
    Max Negative Loss: 1.4004138739293137, Current Negative Loss: 0.11042701567454388, Acquision Function Choose: [1.96536168 2.10579501]
    Get The Better Parameters,The Better Parameters is 1.400805313978457
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.400805313978457, Acquision Function Choose: [ 1.93365025 -2.2556641 ]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.3979972984287454, Acquision Function Choose: [1.29953504 0.54232539]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.0939043446108712, Acquision Function Choose: [-0.38068036 -2.06562496]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 0.8939364303005661, Acquision Function Choose: [-2.56998056  2.99844843]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 0.13214206150821553, Acquision Function Choose: [2.55253525 1.91786163]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.1746428199550532, Acquision Function Choose: [ 1.8168581  -2.99767523]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.3733177635306628, Acquision Function Choose: [1.71648361 1.54278277]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.3358023444107343, Acquision Function Choose: [ 1.42019358 -0.49010271]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.168725846608364, Acquision Function Choose: [-3.99838168 -1.68804677]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 0.058913899376049794, Acquision Function Choose: [1.93460191 2.98147873]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.398106500918049, Acquision Function Choose: [ 2.29555733 -0.68877169]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.329378588990567, Acquision Function Choose: [ 2.35313462 -1.84336171]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.3002149289549407, Acquision Function Choose: [-0.56439577  1.92984965]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 0.7732516129150855, Acquision Function Choose: [1.63319868 2.49965534]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.2953332991758844, Acquision Function Choose: [-3.98894673  1.46637528]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 0.05917708923314947, Acquision Function Choose: [2.07093504 0.4800277 ]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.397638247952914, Acquision Function Choose: [ 1.38152958 -2.38502298]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.144433340505932, Acquision Function Choose: [2.1400777  2.57697476]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.3851783186073987, Acquision Function Choose: [ 2.11333252 -2.6276043 ]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.3909545872072449, Acquision Function Choose: [-0.3313938  -2.99845121]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 0.9235628240898787, Acquision Function Choose: [ 3.99724536 -1.14261883]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 0.7469996297861089, Acquision Function Choose: [ 1.87061992 -1.68382147]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.3874009564775398, Acquision Function Choose: [ 1.91806688 -0.71654747]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.395991616690188, Acquision Function Choose: [1.85423292 0.89700053]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.3835858947131334, Acquision Function Choose: [2.07390955 1.60787819]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.3972695271921236, Acquision Function Choose: [ 2.18064283 -0.10623415]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.3741776574277227, Acquision Function Choose: [0.07577565 0.73351352]
    Max Negative Loss: 1.400805313978457, Current Negative Loss: 1.0488567682558252, Acquision Function Choose: [ 2.07608533 -2.99870931]
    '''
